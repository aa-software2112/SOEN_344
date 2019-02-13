import uuid

from .cart import Cart

class Patient:

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
        self.cart = Cart()

    def add_walkin_to_cart(self, walkin):
        self.cart.add_walk_in(walkin)

    def add_annual_to_cart(self, annual):
        self.cart.add_annual(annual)

    def remove_walkin_from_cart(self, availability_id):
        self.cart.remove_walkin_appointment(availability_id)

    def remove_annual_from_cart(self):
        self.cart.remove_annual_appt()

    def get_walkins_from_ids(self,availability_ids):
        """Availability_ids is a list of integers
        :returns a list of WalkinAppointment object"""
        self.cart.get_walkin_appts(availability_ids)


        