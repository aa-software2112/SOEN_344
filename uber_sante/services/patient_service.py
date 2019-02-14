from app.models.patient import Patient


class PatientService:

    def __init__(self, db):
        self.db = db.get_instance(False)

    def get_patient(self, patient_id):
        """Query the db for a patient by id and return the created patient object"""
        select_stmt = 'SELECT * FROM Patient WHERE id = ?'
        params = (patient_id,)
        result = self.db.return_single(select_stmt, params)

        if result is None:
            return

        patient = Patient(result['id'], result['first_name'], result['last_name'], result['health_card_nb'],
                          result['date_of_birth'],
                          result['gender'], result['phone_nb'], result['home_address'], result['email'])

        return patient

    """
    def insert_patient(self, patient):
        patient = patient.__dict__

        insert_stmt = 'INSERT INTO Patient(id, health_card_nb, date_of_birth, gender, ' \
                      'phone_nb, home_address, email, first_name, last_name)' \
                      'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        params = (patient['id'], patient['health_card_nb'], patient['date_of_birth'], patient['gender'],
                      patient['phone_nb'], patient['home_address'], patient['email'], patient['email'], patient['last_name'])

        self.db.return_none(insert_stmt, params)
    """

