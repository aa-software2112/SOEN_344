

class Nurse:

    def __init__(self, id, access_id, first_name, last_name, clinic_id):
        self.id = id
        self.access_id = access_id
        self.first_name = first_name
        self.last_name = last_name
        self.clinic_id = clinic_id

    def __dict__(self):
        return {
            'id': self.id,
            'access_id': self.access_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'clinic_id': self.clinic_id
        }