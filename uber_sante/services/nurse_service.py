from enum import Enum

from uber_sante.models.nurse import Nurse

from uber_sante.utils.dbutil import DBUtil
from uber_sante.utils.cache import get_from_cache, set_to_cache

class CreateNurseStatus(Enum):
    ACCESS_ID_ALREADY_EXISTS = 1
    SUCCESS = 2

class NurseService:

    def __init__(self):
        self.db = DBUtil.get_instance()

    def test_and_set_nurse_into_cache(self, nurse_id):
        """
        If the doctor object is stored in cache already, don't do anything.
        Otherwise create a new doctor object and store it in cache.
        """
        nurse_key = "nurse"+str(nurse_id)

        if get_from_cache(nurse_key) is not None:
            return

        else:
            select_stmt = '''SELECT * FROM Nurse
                             WHERE id = ?'''
            params = (nurse_id,)
            result = self.db.read_one(select_stmt, params)
            nurse = Nurse(result['id'], result['access_id'], result['first_name'], result['last_name'], result['clinic_id'])

            set_to_cache(nurse_key, nurse)

    def validate_login_info(self, access_id, password):

        select_stmt = '''SELECT 
                            id, 
                            password 
                        FROM Nurse 
                        WHERE access_id = ?'''
        params = (access_id,)

        result = self.db.read_one(select_stmt, params)

        if result is None:
            return -1

        if password != result['password']:
            return -1

        return result['id']

    def create_nurse(self, access_id, first_name, last_name, password, clinic_id):

        # Check if physician permit number already exists
        select_stmt = '''SELECT
                            id
                        FROM Nurse
                        WHERE access_id = ?'''
        params = (access_id,)

        if self.db.read_one(select_stmt, params) is not None:
            return CreateNurseStatus.ACCESS_ID_ALREADY_EXISTS

        insert_stmt = '''INSERT INTO Nurse(
                            access_id,
                            first_name,
                            last_name,
                            password,
                            clinic_id)
                      VALUES (?, ?, ?, ?, ?)'''
        params = (access_id, first_name, last_name, password, clinic_id)

        self.db.write_one(insert_stmt, params)

        return CreateNurseStatus.SUCCESS
