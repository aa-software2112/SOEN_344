import uuid

class doctor:

    def __init__(self, f_name, l_name, ppn, specialty, city):
        self.id = uuid.uuid4()
        self.physician_permit_nb = ppn
        self.first_name = f_name
        self.last_name = l_name
        self.specialty = specialty
        self.city = city