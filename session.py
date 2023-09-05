from datetime import datetime
from decimal import Decimal

class Session:
    """
    Represents a charging session.

    Args:
        chargingStationId (str): The ID of the charging station.
        serial (str): The serial number of the session.
        rfidCard (str): The RFID card associated with the session.
        status (str): The status of the session.
        start (str): The start time of the session in the format "%d-%m-%Y %H:%M:%S".
        end (str): The end time of the session in the format "%d-%m-%Y %H:%M:%S".
        meterAtStart (str): The meter reading at the start of the session (in Wh).
        meterAtEnd (str): The meter reading at the end of the session (in Wh).

    Attributes:
        chargingStationId (str): The ID of the charging station.
        serial (str): The serial number of the session.
        rfidCard (str): The RFID card associated with the session.
        status (str): The status of the session.
        start (datetime): The start time of the session as a datetime object.
        end (datetime): The end time of the session as a datetime object.
        duration (timedelta): The duration of the session as a timedelta object.
        meterAtStart (Decimal): The meter reading at the start of the session (in kWh).
        meterAtEnd (Decimal): The meter reading at the end of the session (in kWh).
        consumption (Decimal): The energy consumption during the session (in kWh).
    """
    def __init__(self, chargingStationId, serial, rfidCard, status, start, end, meterAtStart, meterAtEnd):
        try:
            self.chargingStationId = chargingStationId
            self.serial = serial
            self.rfidCard = rfidCard
            self.status = status
            self.start: datetime = datetime.strptime(start, "%d-%m-%Y %H:%M:%S")
            self.end: datetime = datetime.strptime(end, "%d-%m-%Y %H:%M:%S")
            self.duration = self.end - self.start  # timedelta
            self.meterAtStart = Decimal(meterAtStart) / 1000  # kWh
            self.meterAtEnd = Decimal(meterAtEnd) / 1000  # kWh
            self.consumption = self.meterAtEnd - self.meterAtStart  # kWh
        except (ValueError, TypeError) as e:
            raise ValueError("Invalid input data: " + str(e))
