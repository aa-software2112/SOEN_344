from uber_sante.models.cart import Cart

class Patient:

    def __init__(self, patient_id, f_name, l_name, health_card_nb, date_of_birth, gender, phone_nb, address, email):
        self.id = patient_id
        self.first_name = f_name
        self.last_name = l_name
        self.health_card_nb = health_card_nb
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone_nb = phone_nb
        self.home_address = address
        self.email = email
        self.cart = Cart()

    def add_walkin_to_cart(self, walkin):
        self.cart.add_walk_in(walkin)

    def add_annual_to_cart(self, annual):
        self.cart.add_annual(annual)

    def remove_walkin_from_cart(self, availability_id):
        self.cart.remove_walkin_appointment(availability_id)

    def remove_annual_from_cart(self):
        self.cart.remove_annual_appt()

    def get_walkins_from_ids(self, availability_ids):
        """Availability_ids is a list of integers
        :returns a list of WalkinAppointment object"""
        self.cart.get_walkin_appts(availability_ids)

    def get_id(self):
        return self.id

    def __dict__(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'health_card_nb': self.health_card_nb,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'phone_nb': self.phone_nb,
            'home_address': self.home_address,
            'email': self.email,
            'cart': self.cart.__dict__
        }

if __name__ == "__main__":

    p = Patient(1, "frank", "smith", "1234 5678 9012", "24121992", "F", "5144435211", "7331", "frank.smith@gmail.ca")
    print(p.__dict__())