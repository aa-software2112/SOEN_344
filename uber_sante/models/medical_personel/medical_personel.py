from abc import ABC, abstractmethod
from uber_sante.models.medical_personel.medical_personel_factory import MedicalPersonelServiceFactory


class MedicalPersonelInterface(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def execute(self):
        """
        :return: Should return a medical personel object
        """
        pass

class MedicalPersonel():

    service = None

    def __init__(self, medical_personel):
        self.medical_personel = medical_personel
        self.service_factory = MedicalPersonelServiceFactory()

    def register_doctor(self):
        service = self.service_factory.get_service("Doctor")
        ret_val = service.create_doctor(
            self.medical_personel.physician_permit_nb,
            self.medical_personel.first_name,
            self.medical_personel.last_name,
            self.medical_personel.specialty,
            self.medical_personel.city,
            self.medical_personel.password,
            self.medical_personel.clinic_id
        )
        return ret_val

    def register_nurse(self):
        service = self.service_factory.get_service("Nurse")
        ret_val = service.create_nurse(
            self.medical_personel.access_id,
            self.medical_personel.first_name,
            self.medical_personel.last_name,
            self.medical_personel.password,
            self.medical_personel.clinic_id
        )
        return ret_val
