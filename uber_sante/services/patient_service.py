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

    def create_patient(self, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password):

        insert_stmt = 'INSERT INTO Patient(health_card_nb, date_of_birth, gender, ' \
                      'phone_nb, home_address, email, first_name, last_name, password)' \
                      'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        params = (health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)

        self.db.write_one(insert_stmt, params)
