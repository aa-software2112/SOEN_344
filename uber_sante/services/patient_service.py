from uber_sante.models.patient import Patient
from uber_sante.utils.dbutil import DBUtil


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

    def insert_patient(self, patient):
        patient = patient.__dict__

        insert_stmt = 'INSERT INTO Patient(id, health_card_nb, date_of_birth, gender, ' \
                      'phone_nb, home_address, email, first_name, last_name)' \
                      'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        params = (patient['id'], patient['health_card_nb'], patient['date_of_birth'], patient['gender'],
                  patient['phone_nb'], patient['home_address'], patient['email'], patient['email'],
                  patient['last_name'])

        self.db.write_one(insert_stmt, params)
