from uber_sante.models.schedule import *
from uber_sante.utils.date import *
from uber_sante.services.availability_service import AvailabilityService

class RequestEnum(Enum):
    DAILY_REQUEST = "DAILY"
    MONTHLY_REQUEST = "MONTHLY"


class AppointmentRequestType(Enum):
    ANNUAL = "ANNUAL"
    WALKIN = "WALKIN"
    ALL = "ALL"


class ScheduleRequest:

    def __init__(self, request_type, appointment_request_type, date):
        """

        :param request_type: This request should take a request type that
        comes from the Request enum
        :param appointment_request_type: This request should take a booking type
        that comes from the BookingType enum
        :param date: The date of the schedule request (Date object)
        :return: N/A
        """

        self.request_type = request_type

        self.appointment_request_type = appointment_request_type

        self.date_request = date

    def is_monthly_request(self):
        return self.request_type == RequestEnum.MONTHLY_REQUEST

    def is_daily_request(self):
        return self.request_type == RequestEnum.DAILY_REQUEST

    def get_request_date(self):
        return self.date_request

    def is_annual_request(self):
        return self.appointment_request_type == AppointmentRequestType.ANNUAL

    def is_walkin_request(self):
        return self.appointment_request_type == AppointmentRequestType.WALKIN

    def is_walkin_and_annual_request(self):
        return self.appointment_request_type == AppointmentRequestType.ALL

    def get_appointment_request_type_value(self):
        return self.appointment_request_type.value


class Scheduler:
    _instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """

        if Scheduler._instance is None:
            Scheduler._instance = Scheduler()

        return Scheduler._instance

    def __init__(self):

        if Scheduler._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Scheduler._instance = self

        # TODO should be replaced with singleton: AvailabilityService.get_instance()
        self.availability_service = AvailabilityService()

    def get_schedule(self, schedule_request, av=None):
        """
        This method takes a schedule request, given by a ScheduleRequest object, and creates a
        Daily or Monthly schedule from it.

        :param schedule_request: The schedule request from which a Daily or Monthly schedule will be constructed
        :param av: A list of availabilites - this parameter should be removed once the availability service is implemented;
        it is merely a parameter for being able to inject availabilities without the availability service
        :return: A Schedule object: DailySchedule if schedule_request.is_daily_request(), otherwise MonthlySchedule
        """

        return_schedule = None

        avail = None

        if av == None:
            avail = self.availability_service.get_availabilities(schedule_request)
        else:
            avail = av

        if schedule_request.is_daily_request():

            return_schedule = DailySchedule(avail, schedule_request.get_request_date())

        elif schedule_request.is_monthly_request():

            return_schedule = MonthlySchedule(avail, schedule_request.get_request_date())

        return return_schedule

    def reserve_appointment(self, appointment):
        """
        This method converts an appointment into a booking using the availability service

        :param appointment: The appointment object to convert into a booking
        :return: True if successfully booked, False otherwise
        """
        # Method call returns a boolean that describe whether the availability was successfully reserved
        return self.availability_service.validate_availability_and_reserve(appointment.availability.id)

    def free_availabilities(self, availability_keys):
        """
        Uses the availability service to free the availabilities based on its primary keys (a list of 1 or 3 values)

        :param availability_keys: The availability primary-keys that need to be "freed" - made available again
        :return: N/A
        """

        self.availability_service.free_availabilities(availability_keys)


if __name__ == "__main__":

    sr_daily = ScheduleRequest(RequestEnum.DAILY_REQUEST, Date(2018, DateEnum.APRIL, 16))
    sr_monthly = ScheduleRequest(RequestEnum.MONTHLY_REQUEST, Date(2019, DateEnum.APRIL, 16))

    monthly_avails = []

    # Get availabilities for a single month
    for repetitions in range(1, 12 + 1):

        for day in range(1, 27 + 1):

            for num_avails in range(1, 15 + 1):
                monthly_avails.append(
                    Availability(-1, -1, num_avails * 3600 + (num_avails + repetitions) * 20, "RM", True, 2018, 7, day))

    # Get availabilities for a single day
    daily_avails = []
    for num_avails in range(1, 15 + 1):
        daily_avails.append(
            Availability(-1, -1, num_avails * 3600 + (num_avails + repetitions) * 20, "RM", True, 2019,
                         DateEnum.APRIL.value, 16))

    # create a monthly schedule
    monthly_schedule = Scheduler.get_instance().get_schedule(sr_monthly, monthly_avails)
    monthly_schedule.display_monthly_schedule()
    print(monthly_schedule.get_schedule_date_string())

    # create a daily schedule
    daily_schedule = Scheduler.get_instance().get_schedule(sr_daily, daily_avails)
    daily_schedule.display_daily_schedule()
