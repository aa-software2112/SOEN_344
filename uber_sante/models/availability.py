from uber_sante.utils.date import Date

class Availability:

    SECONDS_IN_HOUR = 60*60
    SECONDS_IN_MINUTE = 60

    def __init__(self, availability_id, doctor_id, start, room, free, year, month, day):

        # Note, the id comes from the Availability Table
        self.id = availability_id
        self.doctor_id = doctor_id
        self.start = start
        self.free = free
        self.room = room
        self.month = month
        self.day = day
        self.year = year

    def get_start_time_string(self):
        return "{}:{} {}".format(int(self.start/(Availability.SECONDS_IN_HOUR)),
                              int((self.start%Availability.SECONDS_IN_HOUR)/Availability.SECONDS_IN_MINUTE),
                                 "AM" if self.start / (Availability.SECONDS_IN_HOUR) < 12 else "PM")

    def get_day(self):
        return self.day

    def get_date(self):

        return Date( self.year, self.month, self.day)

    def is_free(self):

        return self.free

    def __str__(self):

        return "start {} day {} month {} year {}".format(self.get_start_time_string(),
                                                                    self.day,
                                                                    self.month,
                                                                    self.year)

if __name__ == "__main__":

    a = Availability(5, 6, 12*3600+1380, "GREEN_ROOM", True, 2019, 2, 12)
    print(a.get_start_time_string())