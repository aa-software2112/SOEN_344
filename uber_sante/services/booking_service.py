from uber_sante.models.booking import Booking
from uber_sante.utils.dbutil import import DBUtil
from uber_sante.models.appointment import WalkinAppointment, AnnualAppointment


class BookingService:

    def __init__(self):
        self.db = DBUtil.get_instance(False)

    def write_booking(self, appointment):

        appt_dict = appointment.__dict__
        insert_stmt = 'INSERT INTO Booking(availability_id, doctor_id, patient_id) ' \
                      'VALUES (?, ?, ?)'

        if isinstance(AnnualAppointment, appointment):
            for availability_id in appt_dict['availability_ids']:
                params = (availability_id, appt_dict['doctor_id'], appt_dict['patient_id'])
                self.db.return_none(insert_stmt, params)

        elif isinstance(WalkinAppointment, appointment):
            params = (appt_dict['availability_id'], appt_dict['doctor_id'], appt_dict['patient_id'])
            self.db.return_none(insert_stmt, params)

    def get_booking(self, booking_id):
        select_stmt = 'SELECT * FROM Booking WHERE id = ?'
        params = (booking_id,)
        result = self.db.return_single(select_stmt, params)

        if result is None:
            return

        booking = Booking(result['id'], result['availability_id'], result['doctor_id'], result['patient_id'])

        return booking

    def cancel_booking(self, booking_id):
        delete_stmt = 'DELETE FROM Booking WHERE id = ?'
        params = (booking_id,)
        self.db.return_none(delete_stmt, params)

