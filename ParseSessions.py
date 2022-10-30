import csv
from datetime import datetime
import locale
import time
import requests
import os
from dotenv import load_dotenv
from typing import List
from session import Session
from jinja2 import Environment, FileSystemLoader
from decimal import Decimal

def main():
    load_dotenv()
    download_data()
    locale.setlocale(locale.LC_ALL, "de_DE")
    sessions = parse_csv('chargingsession.csv')
    sessions = list(filter(date_filter, sessions))
    sessions = list(reversed(sessions))
    consumption = map(lambda x: x.consumption, sessions)
    consumption = sum(consumption)
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report.html.j2')
    html = template.render(sessions=sessions, date=prev_month(), consumption=consumption, electricity_rate=Decimal(os.environ.get('electricity_rate')), electricity_basic_price=Decimal(os.environ.get('electricity_basic_price')))

    with open('report.html', 'w') as f:
        f.write(html)

def date_filter(x: Session):
    return x.end.year == prev_month().year and x.end.month == prev_month().month

def prev_month(date=datetime.today()):
    if date.month == 1:
        return date.replace(month=12,year=date.year-1)
    else:
        try:
            return date.replace(month=date.month-1)
        except ValueError:
            return prev_month(date=date.replace(day=date.day-1))

def download_data():
    url = 'http://{}/ajax.php'.format(os.environ.get('webui_ip'))
    body = {'username': os.environ.get('username'),'password': os.environ.get('password')}
    authenticate = requests.post(url, json = body)

    request_timestamp = int(time.time())

    url = 'http://{0}/export.php?chargingsessions&t={1}'.format(os.environ.get('webui_ip'), request_timestamp)
    if authenticate.ok:
        download = requests.get(url, cookies=authenticate.cookies)

    if download.ok:
        open('chargingsession.csv', 'wb').write(download.content)

def parse_csv(csvFilePath) -> List[Session]:
    sessions = []

    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf:
        #load csv file data
        csvReader = csv.DictReader(csvf, delimiter=';')

        #convert each csv row to python dict
        for row in csvReader:
            #add row to json array
            if row['Status'] == "CLOSED":
                s = Session(row['Charging Station ID'], row['Serial'], row['RFID Card'], row['Status'], row['Start'], row['End'], row['Duration'], row['Meter at start (Wh)'], row['Meter at end (Wh)'], row['Consumption'])
                sessions.append(s)
    return sessions

if __name__ == "__main__":
    main()