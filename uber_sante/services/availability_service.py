from uber_sante.utils.dbutil import DBUtil

class AvailabilityService:

    def __init__(self):
        self.db = DBUtil.get_instance(False)

    def get_availabilities(self, schedule_request):
        pass

    def free_availabilities(self, availability_ids):
        for availability_id in availability_ids:
            update_stmt = 'UPDATE Availability SET free = 1 WHERE id = ?'
            params = (availability_id,)
            self.db.return_none(update_stmt, params)

    def validate_availability_and_reserve(self, appointment):
        appointment = appointment.__dict__

        # Check that these availabilities are free
        for availability_id in appointment['availability_ids']:
            select_stmt = "SELECT id FROM Availability WHERE availability_id = ? AND free = 0"
            params = (availability_id,)
            if self.db.return_single(select_stmt, params) is not None
                return False

        # Reserve the availabilities
        for availability_id in appointment['availability_ids']:
            update_stmt = 'UPDATE Availability SET free = 0 WHERE id = ?'
            params = (availability_id,)
            self.db.return_none(update_stmt, params)
        return True
