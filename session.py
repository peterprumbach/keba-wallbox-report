from datetime import datetime
from decimal import Decimal

class Session:
    def __init__(self, chargingStationId, serial, rfidCard, status, start, end, duration, meterAtStart, meterAtEnd, consumption):
        self.chargingStationId = chargingStationId
        self.serial = serial
        self.rfidCard = rfidCard
        self.status = status
        self.start: datetime = datetime.strptime(start, "%d-%m-%Y %H:%M:%S")
        self.end: datetime = datetime.strptime(end, "%d-%m-%Y %H:%M:%S")
        self.duration = self.end-self.start
        self.meterAtStart = Decimal(meterAtStart)/1000
        self.meterAtEnd = Decimal(meterAtEnd)/1000
        self.consumption = (self.meterAtEnd-self.meterAtStart)
