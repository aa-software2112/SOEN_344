import uuid

class Patient(object):

    def __init__(self, f_name, l_name, health_card_nb, date_of_birth, gender, phone_nb, address, email):
        self.id = uuid.uuid4()
        self.first_name = f_name
        self.last_name = l_name
        self.health_card_nb = health_card_nb
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone_nb = phone_nb
        self.home_address = address
        self.email = email
        