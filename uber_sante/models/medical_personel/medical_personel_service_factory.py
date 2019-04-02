from uber_sante.models.doctor import Doctor
from uber_sante.services.doctor_service import DoctorService
from uber_sante.services.nurse_service import NurseService

class MedicalPersonelServiceFactory:

    def __init__(self):
        pass
    
    def get_service(self, factory):

        service = None

        if factory == "Doctor":
            service = DoctorService()
        
        if factory == "Nurse":
            service = NurseService()
    
        return service
