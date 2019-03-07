from tests.test_base import BaseTestClass

from uber_sante.models.scheduler import AppointmentRequestType


class AvailabilityTest(BaseTestClass):
    """
    Assumes the server is running!
    """

    def setUp(self):
        """
        Must call setUp() on BaseTestClass to setup the test application

        :return: N/A
        """
        super(AvailabilityTest, self).setUp()

        self.availability_url = "http://localhost:5000/availability"
        self.modify_availability_url = "http://localhost:5000/availability/modify"

        self.availability = {
            "availability_id": 1,
            "doctor_id": "20",
            "start": "32400",
            "room": "088",
            "year": "2019",
            "month": "2",
            "day": "26",
            "booking_type": AppointmentRequestType.ANNUAL.value
        }

    def test_modify_availability_success(self):

        self.mock_db_read()
        self.mock_db_write()

        resp = self.send_put(self.modify_availability_url, self.availability)

        self.assert_status_code(resp, 201)

    def test_modify_availability_fail(self):

        self.mock_db_read(not None)
        self.mock_db_write()

        resp = self.send_put(self.modify_availability_url, self.availability)

        self.assert_status_code(resp, 500)
