import datetime
from enum import Enum

class DateEnum(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


"""
Helper class responsible for maintaining date-based functionality, and can
be modified to include greater customization as project progresses and demands it
"""
class Date:

    # Index corresponds to that returned by
    # datetime.date(yyyy,mm,dd).weekday()
    get_day_of_week_name = ["Monday", "Tuesday", "Wednesday",
                        "Thursday", "Friday", "Saturday", "Sunday"]

    # Month - 1 = index to name of Month
    get_month_name = ["January", "February", "March", "April", "May",
                        "June", "July", "August", "September", "October",
                            "November", "December"]

    def __init__(self, year, month, day = None):

        self.day = day
        self.month = month.value if type(month) == type(DateEnum.JANUARY) else month
        self.year = year
        self.day_name = None
        self.month_name = Date.get_month_name[int(self.month)-1]

        if self.day is not None:
            self.day_name = Date.get_day_of_week_name[datetime.date(self.year, self.month, self.day).weekday()]

    def get_day(self):

        return self.day

    def get_day_name(self):

        return self.day_name

    def get_month(self):

        return self.month

    def get_year(self):

        return self.year

    def get_date_string(self):

        if self.day_name is not None:

            return "{}, {} of {}, {}".format(self.day_name, self.day,
                                                 self.month_name, self.year)
        else: # Day was not provided - month only

            return "{} {}".format(self.month_name, self.year)

if __name__ == "__main__":


    print(Date(2019,2,13).get_date_string())