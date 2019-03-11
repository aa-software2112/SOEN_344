from enum import Enum

from uber_sante.utils.dbutil import DBUtil

from uber_sante.models.booking import Booking
from uber_sante.models.appointment import Appointment

class BookingStatus(Enum):
    SUCCESS = 1
    NO_BOOKINGS = -1

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

        return BookingStatus.SUCCESS


    def get_booking(self, booking_id):
        
        select_stmt = '''SELECT * FROM Booking
                        WHERE id = ?'''
        params = (booking_id,)
        result = self.db.read_one(select_stmt, params)

        if result is None:
            return BookingStatus.NO_BOOKINGS

        booking = Booking(
            result['id'],
            result['availability_id'],
            result['doctor_id'],
            result['patient_id'])

        return booking

    def get_all_bookings(self):

        select_stmt = '''SELECT * FROM Booking'''
        params = ()
        results = self.db.read_all(select_stmt, params)

        list_of_bookings = []

        for result in results:
            list_of_bookings.append(
                Booking(
                    result['id'],
                    result['availability_id'],
                    result['doctor_id'],
                    result['patient_id']))
        
        return list_of_bookings

    def get_bookings_for_patient(self, patient_id):

        select_stmt = '''SELECT * FROM Booking
                        WHERE patient_id = ?'''
        params = (patient_id, )
        results = self.db.read_all(select_stmt, params)

        list_of_bookings = []

        for result in results:
            list_of_bookings.append(
                Booking(
                    result['id'],
                    result['availability_id'],
                    result['doctor_id'],
                    result['patient_id']))
        
        return list_of_bookings


    def cancel_booking(self, booking_id):

        select_stmt = '''SELECT FROM Booking
                        WHERE id = ?'''
        params = (booking_id,)
        select_result = self.db.read_one(select_stmt, params)

        if select_result is None:
            return BookingStatus.NO_BOOKINGS

        delete_stmt = '''DELETE FROM Booking 
                        WHERE id = ?'''
        self.db.write_one(delete_stmt, params)

        return BookingStatus.SUCCESS


    def cancel_booking_with_availability(self, availability_id):
        
        select_stmt = '''SELECT * FROM Booking WHERE 
                        availability_id = ?'''
        params = (availability_id,)
        result = self.db.read_one(select_stmt, params)
        
        if result is None:
            return BookingStatus.NO_BOOKINGS

        delete_stmt = '''DELETE FROM Booking
                        WHERE availability_id = ?'''
        params = (availability_id,)
        self.db.write_one(delete_stmt, params)

        return BookingStatus.SUCCESS


    def cancel_booking_return_key(self, booking_id):
        
        #retrieving booking's primary key from db
        key_retrieval = '''SELECT
                                availability_id
                            FROM Booking
                            WHERE id = ?'''
        params = (booking_id, )

        f_key_dict = self.db.read_one(key_retrieval, params)
        f_key = f_key_dict['availability_id']
        
        #deleting corresponding booking
        delete_stmt = '''DELETE FROM Booking
                        WHERE id = ?'''
        params = (booking_id,)
        self.db.write_one(delete_stmt, params)

        return f_key

    def get_patient_id_from_availability_id(self, availability_id):
        stmt = '''SELECT patient_id FROM Booking WHERE availability_id = ?'''

        params = (availability_id,)

        self.db.read_one(stmt, params)
