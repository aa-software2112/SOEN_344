import uuid
from app.helpers.date import Date

class Availability:

    def __init__(self, availability_id, doctor_id, start, end, room, year, month, day):

        # Note, the id comes from the Availability Table
        self.id = availability_id
        self.doctor_id = doctor_id
        self.start = start
        self.end = end
        self.room = room
        self.month = month
        self.day = day
        self.year = year

    def getDate(self):

        return Date(self.day, self.month, self.year)
