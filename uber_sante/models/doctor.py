import uuid

class Doctor:

    def __init__(self, id, f_name, l_name, ppn, specialty, city):
        self.id = id
        self.physician_permit_nb = ppn
        self.first_name = f_name
        self.last_name = l_name
        self.specialty = specialty
        self.city = city