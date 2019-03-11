from enum import Enum
from uber_sante.models.cart import Cart
from uber_sante.models.appointment import Appointment
from uber_sante.utils.time_interpreter import TimeInterpreter


class MakeAnnualStatus(Enum):
    SUCCESS = 1
    HAS_ANNUAL_APPOINTMENT = 2
    HAS_THIS_APPOINTMENT_IN_CART = 3


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
        self.login_messages = []

    def update(self, availabilities):
        t = TimeInterpreter()
        for availability in availabilities:
            day = str(availability.day)
            month = str(availability.month)
            year = str(availability.year)

            message = "Your booking on " + day + "/" + month + "/" + year + " at " + t.get_start_time_string(availability.start) + " got canceled. We are sorry for this inconvenient."
            print(message)
            self.login_messages.append(message)

    def get_login_messages(self):
        return self.login_messages

    def has_annual_appointment(self):
        return self.cart.contains_annual_appointment()

    def make_annual_appointment(self, availability):
        print(self.cart.get_appointments())
        if self.has_annual_appointment():
            return MakeAnnualStatus.HAS_ANNUAL_APPOINTMENT

        else:
            self.add_annual_to_cart(Appointment(self.id, availability))
            return MakeAnnualStatus.SUCCESS

    def make_walkin_appointment(self, availability):
        print(self.cart.get_appointments())
        if self.cart.get_appointment(availability.get_id()) is not None:
            return MakeAnnualStatus.HAS_THIS_APPOINTMENT_IN_CART
        else:
            self.add_walkin_to_cart((Appointment(self.id, availability)))
            return MakeAnnualStatus.SUCCESS

    def add_walkin_to_cart(self, walkin):
        self.cart.add_appointment(walkin)

    def add_annual_to_cart(self, annual):
        self.cart.add_appointment(annual)

    def remove_from_cart(self, availability_id):
        return self.cart.remove_appointment(availability_id)

    def get_from_id(self, availability_ids):
        """Availability_ids is a list of integers
        :returns a list of WalkinAppointment object"""
        self.cart.get_appointment(availability_ids)

    def get_id(self):
        return self.id

    def get_cart(self):
        return self.cart

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
    # p = Patient(1, "frank", "smith", "1234 5678 9012", "24121992", "F", "5144435211", "7331", "frank.smith@gmail.ca")
    # print(p.__dict__)

    t = TimeInterpreter()
    print(t.get_start_time_string(32400))
