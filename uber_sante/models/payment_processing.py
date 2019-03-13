class ProcessVisa:
   
    @staticmethod
    def process(cc_information):
        return True


class ProcessMasterCard:
    
    @staticmethod
    def process(cc_information):
        return True


class ProcessAmericanExpress:
    
    @staticmethod
    def process(cc_information):
        return True


class ProcessOthers:
   
    @staticmethod
    def process(cc_inforamtion):
        return True


class ProcessPayment:

    credit_card_nb = ''
    first_name = ''
    last_name = ''
    ccv = ''
    expiration_date = ''

    def __init__(self):
        return

    def checkout(self, credit_card):

        cc_type = credit_card[1]    
        result = None
        
        if cc_type == 3:
            result = ProcessAmericanExpress.process(credit_card)

        elif cc_type == 4:
            result = ProcessVisa.process(credit_card)
        
        elif cc_type == 5:
            result = ProcessMasterCard.process(credit_card)
        
        else:
            result = ProcessOthers.process(credit_card)
        
        return result