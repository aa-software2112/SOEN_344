from uber_sante.utils.dbutil import DBUtil

from uber_sante.models.booking import Booking
from uber_sante.models.appointment import Appointment


class BookingService:

    def __init__(self):
        self.db = DBUtil.get_instance()

    def write_booking(self, appointment):

        appt_dict = appointment.__dict__
        insert_stmt = '''INSERT INTO Booking(
                            availability_id,
                            doctor_id,
                            patient_id)
                        VALUES (?, ?, ?)'''
        params = (appt_dict['availability'].id, appt_dict['availability'].doctor_id, appt_dict['patient_id'])
        self.db.write_one(insert_stmt, params)

    def get_booking(self, booking_id):
        select_stmt = '''SELECT * FROM Booking
                        WHERE id = ?'''
        params = (booking_id,)
        result = self.db.read_one(select_stmt, params)

        if result is None:
            return

        booking = Booking(
            result['id'],
            result['availability_id'],
            result['doctor_id'],
            result['patient_id'])

        return booking

    def cancel_booking(self, booking_id):
        delete_stmt = '''DELETE FROM Booking 
                        WHERE id = ?'''
        params = (booking_id,)
        self.db.write_one(delete_stmt, params)

    def cancel(self, booking_id):
        
        #retrieving booking's primary key from db
        key_retrieval = 'SELECT availability_id FROM Booking WHERE id = ?'
        params = (booking_id, )
        f_key_dict = self.db.read_one(key_retrieval, params)
        f_key = f_key_dict['availability_id']
        
        #deleting corresponding booking
        delete_stmt = 'DELETE FROM Booking WHERE id = ?'
        params = (booking_id,)
        self.db.write_one(delete_stmt, params)

        return f_key
