from uber_sante.models.medical_personel.medical_personel import MedicalPersonelInterface, MedicalPersonel

class MedicalNurse(MedicalPersonelInterface):
    
    def __init__(self, nurse):
        self.medical_personel = MedicalPersonel(nurse)

    def execute(self):
        ret_val = self.medical_personel.register_nurse()
        return ret_val