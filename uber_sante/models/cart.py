from abc import ABC, abstractmethod


class Cart:
    def __init__(self):
        self.appointments = []
        self.cart_state = CartWithoutAnnualState(self)

    def add_appointment(self, appointment):
        self.cart_state.add_appointment(appointment)

    def get_appointment(self, availability_id):
        """ searches the list of appointment and returns the none that has the specified id"""
        for appointment in self.appointments:
            if appointment.get_availability_id() == availability_id:
                return appointment
        return None

    def get_appointments(self):
        return self.appointments

    def remove_appointment(self, availability_id):
        return self.cart_state.remove_appointment(availability_id)

    def contains_annual_appointment(self):
        return type(self.cart_state) == CartWithAnnualState

    def set_state(self, state):
        self.cart_state = state

    def get_state(self):
        return self.cart_state

    def __dict__(self):
        return {
            'appointments': self.appointments
        }


class CartState(ABC):

    def __init__(self, cart):
        self.cart = cart

    @abstractmethod
    def add_appointment(self, appointment):
        pass

    @abstractmethod
    def remove_appointment(self, availability_id):
        pass


class CartWithoutAnnualState(CartState):

    def add_appointment(self, appointment):
        """ adds an appointment, and if that appointment is of type annual, it will change the cart state"""
        self.cart.appointments.append(appointment)

        if appointment.is_annual_appointment():
            self.cart.set_state(CartWithAnnualState(self.cart))

    def remove_appointment(self, availability_id):
        index = 0

        for appointment in self.cart.appointments:
            if appointment.get_availability_id() == availability_id:
                return self.cart.appointments.pop(index)

            index = index + 1
        return None


class CartWithAnnualState(CartState):

    def add_appointment(self, appointment):
        if appointment.is_annual_appointment():
            print("Cart has annual appointment already")
            return -1

        self.cart.appointments.append(appointment)

    def remove_appointment(self, availability_id):
        """removes an appointment and if that appointment was an annual appointment, change the state of the cart"""
        index = 0
        for appointment in self.cart.appointments:

            if appointment.get_availability_id() == availability_id:

                if appointment.is_annual_appointment():
                    self.cart.set_state(CartWithoutAnnualState(self.cart))

                return self.cart.appointments.pop(index)

            index = index + 1
        return None
