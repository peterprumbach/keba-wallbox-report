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
    download_data('chargingsession.csv')
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

def authenticate():
    auth_url = 'http://{}/ajax.php'.format(os.environ.get('webui_ip'))
    body = {'username': os.environ.get('username'), 'password': os.environ.get('password')}
    response = requests.post(auth_url, json=body)
    return response.cookies if response.ok else None

def download_data(outputFile: str):
    download_url = 'http://{}/export.php?chargingsessions&t={}'.format(os.environ.get('webui_ip'), int(time.time()))

    cookies = authenticate()
    if cookies:
        download = requests.get(download_url, cookies=cookies)
        if download.ok:
            with open(outputFile, 'wb') as file:
                file.write(download.content)
            print(f'Data downloaded and saved to {outputFile}')
        else:
            print('Failed to download data.')
    else:
        print('Authentication failed.')

def parse_csv(csvFilePath: str) -> List[Session]:
    """
    Parse a CSV file containing charging session data and return a list of Session objects.

    Args:
        csvFilePath (str): The path to the CSV file to parse.

    Returns:
        List[Session]: A list of Session objects.
    """
    sessions = []

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf, delimiter=';')

        sessions = [
            Session(
                row['Charging Station ID'],
                row['Serial'],
                row['RFID Card'],
                row['Status'],
                row['Start'],
                row['End'],
                row['Meter at start (Wh)'],
                row['Meter at end (Wh)']
            )
            for row in csvReader if row['Status'] == "CLOSED"
        ]

    return sessions

if __name__ == "__main__":
    main()