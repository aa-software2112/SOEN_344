from uber_sante.models.medical_personel.medical_personel import MedicalPersonelInterface, MedicalPersonel

class MedicalDoctor(MedicalPersonelInterface):
    
    def __init__(self, doctor):
        self.medical_personel = MedicalPersonel(doctor)

    def execute(self):
        ret_val = self.medical_personel.register_doctor()
        return ret_val