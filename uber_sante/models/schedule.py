from calendar import monthrange
from abc import ABC, abstractmethod

from uber_sante.utils.date import Date
from uber_sante.models.availability import Availability
from uber_sante.models.scheduler import AppointmentRequestType


class Schedule(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_schedule_date_string(self):
        """

        :return: Should return some date string representing
         the schedule's representation scope (month or day) for front-end display
        """
        pass


class DailySchedule(Schedule):

    def __init__(self, list_of_availabilities, date):
        """

        :param list_of_availabilities: A list of Availability objects corresponding to a single date
        :param date: The Date object corresponding to the list of availabilites
        """
        Schedule.__init__(self)

        self.availabilities = list_of_availabilities

        self.date_of_daily_schedule = date

    def get_schedule_date_string(self):

        return self.date_of_daily_schedule.get_date_string()

    def availability_exists_today(self):
        """
        Checks if there is at-least a single availability in this object that is "free"
        :return: True if there exists a free availability, otherwise False
        """

        availability_exists = False

        for avail in self.availabilities:

            # The availability is free, so one slot exists on this day
            if avail.is_free():
                availability_exists = True

                break

        return availability_exists

    def display_daily_schedule(self):

        print("\t{}".format(self.get_schedule_date_string()))

        print("\tAvail today?:{}".format(self.availability_exists_today()))

        for avail in self.availabilities:
            print("\t\t{}".format(avail))

    def as_dict(self):
        dict = {}

        for availability in self.availabilities:
            dict[availability.get_id()] = availability.__dict__

        return dict


class MonthlySchedule(Schedule):

    def __init__(self, list_of_availabilities, date):
        """
        This class contains a dictionary of DailySchedules, where each key in the dictionary
        corresponds to the day of the month, and the value is the DailySchedule itself. This will
        help render a monthly schedule to the front end

        :param list_of_availabilities: A list of availabilities for an entire month
        :param date: The date that represents the month - the day attribute need not be set: Note
        that the month described by this date object should be the same as the month covered by the
        list_of_availabilities
        """
        Schedule.__init__(self)

        self.daily_schedules = {}

        number_of_days_in_month = monthrange(date.get_year(), date.get_month())[1]

        # The minimum and maximum keys of the dictionary of DailySchedules
        self.min_date_key = 1

        self.max_date_key = number_of_days_in_month

        # Generates all dictionary keys for all days in the month
        for day in range(self.min_date_key, self.max_date_key + 1):
            self.daily_schedules[day] = None

        self.date_of_monthly_schedule = date

        self.create_all_daily_schedules(list_of_availabilities)

    def create_all_daily_schedules(self, list_of_availabilities):

        avail_dict = self.daily_schedules.copy()

        # Create a list for each key
        for k, v in avail_dict.items():
            avail_dict[k] = []

        # Loop over all availabilities, separating them into lists by date of
        # availability
        for avail in list_of_availabilities:
            # Expect integer days
            avail_dict[int(avail.get_day())].append(avail)

        # Get list of availabilities by day, and create daily schedules of them
        for day, v in avail_dict.items():
            self.daily_schedules[day] = DailySchedule(avail_dict[day], Date(self.date_of_monthly_schedule.get_year(),
                                                                            self.date_of_monthly_schedule.get_month(),
                                                                            day))

    def get_list_of_daily_schedules(self):

        return_list = []

        for day in range(self.min_date_key, self.max_date_key + 1):
            return_list.append(self.daily_schedules[day])

        return return_list

    def get_schedule_date_string(self):

        return self.date_of_monthly_schedule.get_date_string()

    def display_monthly_schedule(self):

        for day in range(self.min_date_key, self.max_date_key + 1):
            self.daily_schedules[day].display_daily_schedule()

    def as_dict(self):
        dict = {}

        for day in range(self.min_date_key, self.max_date_key + 1):
            dict[day] = self.daily_schedules[day].as_dict()

        return dict


if __name__ == "__main__":

    avails = []

    for repetitions in range(1, 12 + 1):

        for day in range(1, 27 + 1):

            for num_avails in range(1, 15 + 1):
                avails.append(
                    Availability(
                        -1,
                        -1,
                        num_avails * 3600 + (num_avails + repetitions) * 20,
                        "RM",
                        True,
                        2018,
                        7,
                        day,
                        AppointmentRequestType.ALL))

    m = MonthlySchedule(avails, Date(2018, 7))

    for sched in m.get_list_of_daily_schedules():
        print("{}, avail?{}".format(sched.get_schedule_date_string(), sched.availability_exists_today()))
