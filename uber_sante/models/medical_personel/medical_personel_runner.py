from enum import Enum
from uber_sante.models.medical_personel.medical_doctor import MedicalDoctor
from uber_sante.models.medical_personel.medical_nurse import MedicalNurse

class MedicalPersonelStatus(Enum):
    SUCCESS = 1
    MISSING_PARAMETERS = -1

class MedicalPersonelRunner:
    
    def __init__(self, request_object):
        self.request_obj = request_object

    def create_medical_personel(self):

        medical_personel = None

        if self.verify_doctor():
            medical_personel = MedicalDoctor(self.request_obj)
            medical_personel.execute()

        elif self.verify_nurse():
            medical_personel = MedicalNurse(self.request_obj)
            medical_personel.execute()

        else:
            return MedicalPersonelStatus.MISSING_PARAMETERS
    
    def verify_doctor(self):

        physician_permit_nb = self.request_obj.get("physician_permit_nb")
        first_name = self.request_obj.get("first_name")
        last_name = self.request_obj.get("last_name")
        specialty = self.request_obj.get("specialty")
        city = self.request_obj.get("city")
        password = self.request_obj.get("password")
        clinic_id = self.request_obj.get("clinic_id")

        if physician_permit_nb is None:
            return MedicalPersonelStatus.MISSING_PARAMETERS
        if first_name is None:
            return MedicalPersonelStatus.MISSING_PARAMETERS
        if last_name is None:
            return MedicalPersonelStatus.MISSING_PARAMETERS
        if specialty is None:
            return MedicalPersonelStatus.MISSING_PARAMETERS
        if city is None:
            return MedicalPersonelStatus.MISSING_PARAMETERS
        if password is None:
            return MedicalPersonelStatus.MISSING_PARAMETERS
        if clinic_id is None:
            return MedicalPersonelStatus.MISSING_PARAMETERS

        return MedicalPersonelStatus.SUCCESS

    def verify_nurse(self):

        access_id = self.request_obj.get("access_id")
        first_name = self.request_obj.get("first_name")
        last_name = self.request_obj.get("last_name")
        password = self.request_obj.get("password")
        clinic_id = self.request_obj.get("clinic_id")

        if access_id is None:
            return MedicalPersonelStatus.MISSING_PARAMETERS
        if first_name is None:
            return MedicalPersonelStatus.MISSING_PARAMETERS
        if last_name is None:
            return MedicalPersonelStatus.MISSING_PARAMETERS
        if password is None:
            return MedicalPersonelStatus.MISSING_PARAMETERS
        if clinic_id is None:
            return MedicalPersonelStatus.MISSING_PARAMETERS

        return MedicalPersonelStatus.SUCCESS