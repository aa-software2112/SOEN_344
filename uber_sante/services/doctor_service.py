from uber_sante.utils.dbutil import DBUtil
from enum import Enum

class CreateDoctorStatus(Enum):
    PHYSICIAN_NUMBER_ALREADY_EXISTS = 1
    SUCCESS = 2

class DoctorService:

    def __init__(self):
        self.db = DBUtil.get_instance()

    def create_doctor(self, physician_permit_nb, first_name, last_name, specialty, city, password):

        # Check if physician permit number already exists
        select_stmt = 'SELECT id FROM Doctor WHERE physician_permit_nb = ?'
        params = (physician_permit_nb,)

        if self.db.read_one(select_stmt, params) is not None:
            return CreateDoctorStatus.PHYSICIAN_NUMBER_ALREADY_EXISTS

        insert_stmt = 'INSERT INTO Doctor(physician_permit_nb, first_name, last_name, ' \
                      'specialty, city, password)' \
                      'VALUES (?, ?, ?, ?, ?, ?)'
        params = (physician_permit_nb, first_name, last_name, specialty, city, password)

        self.db.write_one(insert_stmt, params)

        return CreateDoctorStatus.SUCCESS
