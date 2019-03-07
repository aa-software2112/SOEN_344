from enum import Enum
from uber_sante.utils.cache import get_from_cache, set_to_cache
from uber_sante.models.doctor import Doctor
from uber_sante.utils.dbutil import DBUtil
from uber_sante.models.doctor import Doctor

class CreateDoctorStatus(Enum):
    SUCCESS = 1
    PHYSICIAN_NUMBER_ALREADY_EXISTS = 2
    DOCTOR_ID_DOES_NOT_EXIST = 3
    DOCTOR_NAME_DOES_NOT_EXIST = 4

class DoctorService:

    def __init__(self):
        self.db = DBUtil.get_instance()

    def test_and_set_doctor_into_cache(self, doctor_id):
        """
        If the doctor object is stored in cache already, don't do anything.
        Otherwise create a new doctor object and store it in cache.
        """
        doctor_key = "doctor"+str(doctor_id)

        if get_from_cache(doctor_key) is not None:
            return

        else:
            select_stmt = "SELECT * FROM Doctor WHERE id = ?"
            params = (doctor_id,)
            result = self.db.read_one(select_stmt, params)
            doctor = Doctor(result['id'], result['first_name'], result['last_name'], result['physician_permit_nb'],
                            result['specialty'], result['city'])


            set_to_cache(doctor_key, doctor)

    def validate_login_info(self, physician_permit_nb, password):

        if physician_permit_nb.isdigit():
            physician_permit_nb = int(physician_permit_nb)
        else:
            return -1

        select_stmt = 'SELECT id, password FROM Doctor WHERE physician_permit_nb = ?'
        params = (physician_permit_nb,)

        result = self.db.read_one(select_stmt, params)

        if result is None:
            return -1

        if password != result['password']:
            return -1

        return result['id']

    def create_doctor(self, physician_permit_nb, first_name, last_name, specialty, city, password):

        # Check if physician permit number already exists
        select_stmt = '''SELECT 
                            id
                        FROM Doctor
                        WHERE physician_permit_nb = ?'''
        params = (physician_permit_nb,)

        if self.db.read_one(select_stmt, params) is not None:
            return CreateDoctorStatus.PHYSICIAN_NUMBER_ALREADY_EXISTS

        insert_stmt = '''INSERT INTO Doctor(
                            physician_permit_nb,
                            first_name,
                            last_name,
                            specialty,
                            city,
                            password)
                        VALUES (?, ?, ?, ?, ?, ?)'''
        params = (physician_permit_nb, first_name, last_name, specialty, city, password)

        self.db.write_one(insert_stmt, params)

        return CreateDoctorStatus.SUCCESS


    def get_doctor(self, doctor_id):

        select_stmt = '''SELECT * FROM Doctor
                        WHERE doctor_id = ?'''
        params = (doctor_id,)
        result = self.db.read_one(select_stmt, params)

        if result is None:
            return 3
        
        doctor = Doctor(
            result['id'],
            result['physician_permit_nb'],
            result['first_name'],
            result['last_name'],
            result['specialty'],
            result['city'],
            result['password'])

        return doctor


    def get_doctor_by_name(self, doctor_last_name):

        select_stmt = """SELECT * FROM Doctor
                        WHERE last_name LIKE '%?%' """
        params = (doctor_last_name,)
        results = self.db.read_all(select_stmt, params)

        if results is None:
            return 4
        
        list_of_doctors = []

        for result in results:
            list_of_doctors.append(
                Doctor(
                    result['id'],
                    result['physician_permit_nb'],
                    result['first_name'],
                    result['last_name'],
                    result['specialty'],
                    result['city'],
                    result['password']))
        
        return list_of_doctors