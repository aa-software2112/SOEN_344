from enum import Enum

from uber_sante.utils.dbutil import DBUtil
from uber_sante.utils.cache import get_from_cache, set_to_cache

from uber_sante.models.patient import Patient


class CreatePatientStatus(Enum):
    SUCCESS = 1
    HEALTH_CARD_ALREADY_EXISTS = -1
    EMAIL_ALREADY_EXISTS = -2
    PATIENT_NAME_DOES_NOT_EXIST = -3


class PatientService:

    def __init__(self):
        self.db = DBUtil.get_instance()

    def get_patient(self, patient_id):
        """Query the db for a patient by id and return the created patient object"""

        select_stmt = '''SELECT * FROM Patient
                        WHERE id = ?'''
        params = (patient_id,)
        result = self.db.read_one(select_stmt, params)

        if result is None:
            return

        patient = Patient(
            result['id'],
            result['first_name'],
            result['last_name'],
            result['health_card_nb'],
            result['date_of_birth'],
            result['gender'],
            result['phone_nb'],
            result['home_address'],
            result['email'])

        return patient
    
    def get_patient_by_last_name(self, last_name):
        """Query the db for a patient by the patient's last name and return the created patient object"""
        last_name_formatted = '%' + last_name + '%'
        select_stmt = """SELECT * FROM Patient
                        WHERE last_name LIKE ?"""
        params = (last_name_formatted,)
        results = self.db.read_all(select_stmt, params)

        if len(results) == 0:
            return -3

        list_of_patient = []

        for result in results:
            list_of_patient.append(
                Patient(
                    result['id'],
                    result['first_name'],
                    result['last_name'],
                    result['health_card_nb'],
                    result['date_of_birth'],
                    result['gender'],
                    result['phone_nb'],
                    result['home_address'],
                    result['email']))
        
        return list_of_patient

    def get_patient_by_health_card_nb(self, health_card_nb):
        """Query the db for a patient by the patient's health card nb and return the created patient object"""

        select_stmt = '''SELECT *
                        FROM Patient
                        WHERE health_card_nb = ?'''
        params = (health_card_nb, )
        result = self.db.read_one(select_stmt, params)

        if len(result) == 0:
            return -3

        self.test_and_set_patient_into_cache(result['id'])
        patient = get_from_cache(result['id'])

        return patient

    def validate_login_info(self, health_card_nb, password):

        select_stmt = '''SELECT
                            id,
                            password
                        FROM Patient
                        WHERE health_card_nb = ?'''
        params = (health_card_nb,)

        result = self.db.read_one(select_stmt, params)

        if result is None:
            "Wrong health card number!"
            return -1

        if password != result['password']:
            "Wrong password!"
            return -1

        return result['id']

    def test_and_set_patient_into_cache(self, patient_id):
        """
        If the patient object is stored in cache already, don't do anything.
        Otherwise create a new patient object and store it in cache.
        """

        if get_from_cache(patient_id) is not None:
            return

        else:
            select_stmt = '''SELECT * FROM Patient
                            WHERE id = ?'''
            params = (patient_id,)
            result = self.db.read_one(select_stmt, params)

            patient = Patient(
                result['id'],
                result['first_name'],
                result['last_name'],
                result['health_card_nb'],
                result['date_of_birth'],
                result['gender'],
                result['phone_nb'],
                result['home_address'],
                result['email'])

            set_to_cache(patient_id, patient)

    def create_patient(self, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name,last_name, password):

        # Check if health card already exists in db
        select_stmt = '''SELECT
                            id
                        FROM Patient
                        WHERE health_card_nb = ?'''
        params = (health_card_nb,)
        if self.db.read_one(select_stmt, params) is not None:
            return CreatePatientStatus.HEALTH_CARD_ALREADY_EXISTS

        # Check if email already exists in db
        select_stmt = '''SELECT
                            id
                        FROM Patient
                        WHERE email = ?'''
        params = (email,)
        if self.db.read_one(select_stmt, params) is not None:
            return CreatePatientStatus.EMAIL_ALREADY_EXISTS

        else:
            insert_stmt = '''INSERT INTO Patient(
                                health_card_nb,
                                date_of_birth,
                                gender,
                                phone_nb,
                                home_address,
                                email,
                                first_name,
                                last_name,
                                password)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            params = (health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)

            self.db.write_one(insert_stmt, params)

            return CreatePatientStatus.SUCCESS


    def update_patient(self, patient_id, date_of_birth, gender, phone_nb, home_address, first_name,last_name, password):

        insert_stmt = '''UPDATE Patient
                        SET date_of_birth = ?,
                            gender = ?,
                            phone_nb = ?,
                            home_address = ?,
                            first_name = ?,
                            last_name = ?,
                            password = ?
                        WHERE id = ?
                        '''
        params = (date_of_birth, gender, phone_nb, home_address, first_name, last_name, password, patient_id)
        
        self.db.write_one(insert_stmt, params)

        return CreatePatientStatus.SUCCESS
