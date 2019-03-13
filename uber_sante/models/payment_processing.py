from abc import ABC, abstractmethod

class PaymentStrategy(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def make_payment(self, cc_information):
        """
        :param cc_information: Credit card information
        :return: True/False for successful payment
        """

class VisaPaymentStrategy(PaymentStrategy):

    def __init__(self):
        PaymentStrategy.__init__(self)

    def make_payment(self, cc_information):
        print("Stub Method: Paying with Visa")
        return True


class MastercardStrategy(PaymentStrategy):
    def __init__(self):
        PaymentStrategy.__init__(self)

    def make_payment(self, cc_information):
        print("Stub Method: Paying with Mastercard")
        return True


class AmericanExpressStrategy(PaymentStrategy):
    def __init__(self):
        PaymentStrategy.__init__(self)

    def make_payment(self, cc_information):
        print("Stub Method: Paying with American Express")
        return True


class OtherPaymentStrategy(PaymentStrategy):
    def __init__(self):
        PaymentStrategy.__init__(self)

    def make_payment(self, cc_information):
        print("Stub Method: Paying with Other")
        return True

class ProcessPayment:

    def __init__(self, as_stub=True):
        self.strategy = None
        self.as_stub = as_stub
        self.stub_cc = "3234567890123456"
        pass

    def checkout(self, credit_card):

        if self.as_stub:
            credit_card = self.stub_cc

        if not(isinstance(credit_card, str) and len(credit_card)==16):
            return False

        cc_type = int(credit_card[0])

        if cc_type == 3:
            self.set_strategy(AmericanExpressStrategy())
        elif cc_type == 4:
            self.set_strategy(VisaPaymentStrategy())
        elif cc_type == 5:
            self.set_strategy(MastercardStrategy())
        else:
            self.set_strategy(OtherPaymentStrategy())

        return self.make_payment(credit_card)

    def set_strategy(self, strat):

        if isinstance(strat, PaymentStrategy):
            self.strategy = strat

    def make_payment(self, cc_information):

        if self.strategy is None:
            return False
        return self.strategy.make_payment(cc_information)


if __name__ == "__main__":

    credit_card_american_express = "3234567890123456"
    credit_card_visa = "4234567890123456"
    credit_card_master_card = "5234567890123456"
    credit_card_other = "6234567890123456"
    ProcessPayment(as_stub=False).checkout(credit_card_american_express)
    ProcessPayment(as_stub=False).checkout(credit_card_visa)
    ProcessPayment(as_stub=False).checkout(credit_card_master_card)
    ProcessPayment(as_stub=False).checkout(credit_card_other)