from uber_sante.utils.dbutil import DBUtil
from uber_sante.models.appointment import WalkinAppointment, AnnualAppointment
from uber_sante.models.availability import Availability


class AvailabilityService:

    def __init__(self):
        self.db = DBUtil.get_instance()

    def get_availabilities(self, schedule_request):
        """
        Queries the Availability table according to the schedule_request object
        which specifies to query for the month or for a specific day only,
        and for annual, walkin, or all booking types.
        """

        date = schedule_request.get_request_date()
        year = date.get_year()
        month = date.get_month()
        booking_type = schedule_request.get_appointment_request_type_value()

        if schedule_request.is_daily_request():

            day = date.get_day()

            # If the booking_type is BookingType.ALL (which has value ""), it will select all rows
            select_stmt = 'SELECT * FROM Availability ' \
                          'WHERE year = ? AND month = ? AND day = ?' \
                          'AND (? = "ALL" OR booking_type = ?)'

            params = (year, month, day, booking_type, booking_type)

        elif schedule_request.is_monthly_request():

            # If the booking_type is BookingType.ALL (which has value ""), it will select all rows
            select_stmt = 'SELECT * FROM Availability ' \
                          'WHERE year = ? AND month = ?' \
                          'AND (? = "ALL" OR booking_type = ?)'

            params = (year, month, booking_type, booking_type)

        results = self.db.read_all(select_stmt, params)

        list_of_availabilities = []

        for result in results:
            list_of_availabilities.append(Availability(result['id'], result['doctor_id'], result['start'],
                                                       result['room'], result['free'], result['year'], result['month'],
                                                       result['day']))

        return list_of_availabilities

    """
    def free_availabilities(self, availability_ids):

        for availability_id in availability_ids:
            update_stmt = 'UPDATE Availability SET free = 1 WHERE id = ?'
            params = (availability_id,)
            self.db.write_one(update_stmt, params)
    """

    def free_availability(self, availability_id):

        update_stmt = 'UPDATE Availability SET free = 1 WHERE id = ?'
        params = (availability_id, )
        self.db.write_one(update_stmt, params)

    def validate_availability_and_reserve(self, appointment):
        """
        Given either a Walkin (20min, 1 row) or Annual appointment (60min, 3 rows),
        checks the DB to see whether the availability is free,
        and if so, it reserves it.
        """

        availability_id = appointment.__dict__['availability_ids'][0] if isinstance(appointment, AnnualAppointment) \
            else appointment.__dict__['availability_id']

        select_stmt = "SELECT id FROM Availability WHERE availability_id = ? AND free = 0"

        update_stmt = 'UPDATE Availability SET free = 0 WHERE id = ?'

        params = (availability_id, )

        i = 3 if isinstance(appointment, AnnualAppointment) else 1

        for x in range(0, i):
            if self.db.read_one(select_stmt, params) is not None:
                return False

        for x in range(0, i):
            self.db.write_one(update_stmt, params)
        return True
