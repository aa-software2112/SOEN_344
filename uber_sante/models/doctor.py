class Doctor:

    def __init__(self, doctor_id, f_name, l_name, ppn, specialty, city, password, clinic_id):
        self.id = doctor_id
        self.physician_permit_nb = ppn
        self.first_name = f_name
        self.last_name = l_name
        self.specialty = specialty
        self.city = city
        self.password = password
        self.clinic_id = clinic_id

    
    def __dict__(self):
        return {
            'id': self.id,
            'physician_permit_nb': self.physician_permit_nb,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'specialty': self.specialty,
            'city': self.city,
            'password': self.password,
            'clinic_id': self.clinic_id
        }