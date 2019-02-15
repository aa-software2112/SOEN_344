from uber_sante.utils.dbutil import DBUtil
from uber_sante.models.appointment import WalkinAppointment, AnnualAppointment
from uber_sante.models.availability import Availability


class AvailabilityService:

    def __init__(self):
        self.db = DBUtil.get_instance()

    def get_availabilities(self, schedule_request):

        date = schedule_request.get_request_date()
        year = date.get_year()
        month = date.get_month()

        if schedule_request.is_daily_request():
            day = date.get_day()
            select_stmt = 'SELECT * FROM Availability WHERE year = ? AND month = ? AND day = ?'
            params = (year, month, day)

        elif schedule_request.is_monthly_request():
            select_stmt = 'SELECT * FROM Availability WHERE year = ? AND month = ?'
            params = (year, month)

        results = self.db.read_all(select_stmt, params)  # Returns a list of the matching rows

        list_of_availabilities = []
        for result in results:
            list_of_availabilities.append(Availability(result['id'], result['doctor_id'], result['start'],
                                                       result['room'], result['free'], result['year'], result['month'],
                                                       result['day']))

        return list_of_availabilities

    def free_availabilities(self, availability_ids):

        for availability_id in availability_ids:
            update_stmt = 'UPDATE Availability SET free = 1 WHERE id = ?'
            params = (availability_id,)
            self.db.write_one(update_stmt, params)

    def validate_availability_and_reserve(self, appointment):

        appt_dict = appointment.__dict__
        select_stmt = "SELECT id FROM Availability WHERE availability_id = ? AND free = 0"
        update_stmt = 'UPDATE Availability SET free = 0 WHERE id = ?'

        if isinstance(appointment, AnnualAppointment):
            # Check that these availabilities are free
            for availability_id in appt_dict['availability_ids']:
                params = (availability_id,)
                if self.db.read_one(select_stmt, params) is not None:
                    return False

            # Reserve the availabilities
            for availability_id in appt_dict['availability_ids']:
                params = (availability_id,)
                self.db.write_one(update_stmt, params)
            return True

        elif isinstance(appointment, WalkinAppointment):

            availability_id = appt_dict['availability_id']
            params = (availability_id,)
            if self.db.read_one(select_stmt, params) is not None:
                return False

            else:
                self.db.write_one(update_stmt, params)
                return True
