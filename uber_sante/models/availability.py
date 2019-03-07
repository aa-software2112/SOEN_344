from uber_sante.utils.date import Date
from uber_sante.utils.time_interpreter import TimeInterpreter


class Availability:

    def __init__(self, availability_id, doctor_id, start, room, free, year, month, day, booking_type):

        # Note, the id comes from the Availability Table
        self.id = availability_id
        self.doctor_id = doctor_id
        self.start = start
        self.free = free
        self.room = room
        self.month = month
        self.day = day
        self.year = year
        # either AppointmentRequestType.WALKIN or AppointmentRequestType.ANNUAL
        self.booking_type = booking_type

    def get_id(self):
        return self.id

    def get_day(self):
        return self.day

    def get_start(self):
        return self.start

    def get_date(self):

        return Date( self.year, self.month, self.day)

    def is_free(self):

        return self.free

    def get_booking_type(self):
        return self.booking_type

    def __str__(self):

        return "start {} day {} month {} year {}".format(TimeInterpreter.get_start_time_string(self.start),
                                                                    self.day,
                                                                    self.month,
                                                                    self.year)

if __name__ == "__main__":

    a = Availability(5, 6, 12*3600+1380, "GREEN_ROOM", True, 2019, 2, 12)
    print(TimeInterpreter.get_start_time_string(a.get_start()))