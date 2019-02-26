from uber_sante.services.patient_service import PatientService
from uber_sante.models.appointment import Appointment
from uber_sante.models.availability import Availability
from uber_sante.models.scheduler import AppointmentRequestType
from tests.test_base import BaseTestClass
from uber_sante.utils import cache
from uber_sante.utils.dbutil import DBUtil

class BookingTest(BaseTestClass):
    """
    Assumes the server is running!
    """

    def setUp(self):
        """
        Must call setUp() on BaseTestClass to setup the test application

        :return: N/A
        """

        super(BookingTest, self).setUp()
        self.booking_url = "http://localhost:5000/booking"
        self.patient_id = "16"
        self.availability_id = "20"
        cache.reset_cache()
        DBUtil.get_instance().reinstantiate_db()

    def test_checkout_endpoint_success(self):
        """
        Testing login endpoint, and logged in successfully

        :return: N/A
        """
        PatientService().test_and_set_patient_into_cache(self.patient_id)
        patient = cache.get_from_cache(self.patient_id)

        availability = Availability(self.availability_id, "20", "32400", "881", "1", "2019", "4", "8", AppointmentRequestType.WALKIN)
        appointment = Appointment(self.patient_id, availability)

        patient.add_walkin_to_cart(appointment)

        valid_info = {"patient_id": self.patient_id, "availability_id":self.availability_id}

        response = self.send_put(self.booking_url, valid_info)

        self.assert_status_code(response, 200)
        self.assert_json_message(response, "Appointment successfully booked")




