from uber_sante.models.patient import Patient
from uber_sante.utils.dbutil import DBUtil
from uber_sante.utils.cache import get_from_cache, set_to_cache


class PatientService:

    def __init__(self):
        self.db = DBUtil.get_instance()

    def get_patient(self, patient_id):
        """Query the db for a patient by id and return the created patient object"""
        select_stmt = 'SELECT * FROM Patient WHERE id = ?'
        params = (patient_id,)
        result = self.db.read_one(select_stmt, params)

        if result is None:
            return

        patient = Patient(result['id'], result['first_name'], result['last_name'], result['health_card_nb'],
                          result['date_of_birth'],
                          result['gender'], result['phone_nb'], result['home_address'], result['email'])

        return patient

    def validate_login_info(self, health_card_nb, password):

        select_stmt = 'SELECT id, password FROM Patient WHERE health_card_nb = ?'
        params = (health_card_nb,)

        result = self.db.read_one(select_stmt, params)

        if result is None:
            "Wrong health card number!"
            return -1

        if password != result['password']:
            "Wrong password!"
            return -1

        return result['id']

    def test_and_set_patient_into(self, patient_id):
        """
        If the patient object is stored in cache already, don't do anything.
        Otherwise create a new patient object and store it in cache.
        """

        if get_from_cache(patient_id) is not None:
            return

        else:
            select_stmt = "SELECT * FROM Patient WHERE id = ?"
            params = (patient_id,)
            result = self.db.read_one(select_stmt, params)

            patient = Patient(result['id'], result['first_name'], result['last_name'], result['health_card_nb'],
                              result['date_of_birth'], result['gender'], result['phone_nb'], result['home_address'],
                              result['email'])

            set_to_cache(patient_id, patient)

    def create_patient(self, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name,
                       last_name, password):

        insert_stmt = 'INSERT INTO Patient(health_card_nb, date_of_birth, gender, ' \
                      'phone_nb, home_address, email, first_name, last_name, password)' \
                      'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        params = (health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)

        self.db.write_one(insert_stmt, params)
