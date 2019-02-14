from uber_sante.utils.dbutil import DBUtil
from uber_sante.models.appointment import WalkinAppointment, AnnualAppointment


class AvailabilityService:

    def __init__(self):
        self.db = DBUtil.get_instance()

    def get_availabilities(self, schedule_request):
        pass

    def free_availabilities(self, availability_ids):
        for availability_id in availability_ids:
            update_stmt = 'UPDATE Availability SET free = 1 WHERE id = ?'
            params = (availability_id,)
            self.db.return_none(update_stmt, params)

    def validate_availability_and_reserve(self, appointment):

        appt_dict = appointment.__dict__
        select_stmt = "SELECT id FROM Availability WHERE availability_id = ? AND free = 0"
        update_stmt = 'UPDATE Availability SET free = 0 WHERE id = ?'

        if isinstance(AnnualAppointment, appointment):
            # Check that these availabilities are free
            for availability_id in appt_dict['availability_ids']:
                params = (availability_id,)
                if self.db.return_single(select_stmt, params) is not None:
                    return False
            # Reserve the availabilities
            for availability_id in appt_dict['availability_ids']:
                params = (availability_id,)
                self.db.return_none(update_stmt, params)
            return True

        elif isinstance(WalkinAppointment, appointment):
            availability_id = appt_dict['availability_id']
            params = (availability_id,)
            if self.db.return_single(select_stmt, params) is not None:
                return False
            else:
                self.db.return_none(update_stmt, params)
                return True
