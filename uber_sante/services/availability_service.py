from enum import Enum
import uber_sante
from uber_sante.utils.dbutil import DBUtil
from uber_sante.utils.time_interpreter import TimeInterpreter

from uber_sante.models.availability import Availability

convert_time = TimeInterpreter()

class AvailabilityStatus(Enum):
    SUCESS = 1
    NO_AVAILABILITIES_FOR_DOCTOR = 2   # no availabilities for a particular doctor
    NO_AVAILABILITIES_AT_THIS_HOUR = 3
    

class AvailabilityService:

    def __init__(self):
        self.db = DBUtil.get_instance()


    def get_availabilities(self, schedule_request):
        """
        Queries the Availability table according to the schedule_request object
        which specifies to query for the month or for a specific day only,
        and for annual, walkin, or all booking types.
        """

        date = schedule_request.get_request_date()
        year = date.get_year()
        month = date.get_month()
        appointment_request_type = schedule_request.get_appointment_request_type_value()

        if schedule_request.is_daily_request():

            day = date.get_day()

            # If the booking_type is BookingType.ALL (which has value ""), it will select all rows
            select_stmt = '''SELECT * FROM Availability
                            WHERE year = ?
                            AND month = ?
                            AND day = ?
                            AND (? = "ALL" OR booking_type = ?)'''
            params = (year, month, day, appointment_request_type, appointment_request_type)

        elif schedule_request.is_monthly_request():

            # If the booking_type is BookingType.ALL (which has value ""), it will select all rows
            select_stmt = '''SELECT * FROM Availability
                          WHERE year = ?
                          AND month = ?
                          AND (? = "ALL" OR booking_type = ?)'''
            params = (year, month, appointment_request_type, appointment_request_type)

        results = self.db.read_all(select_stmt, params)

        list_of_availabilities = []

        for result in results:
            list_of_availabilities.append(
                Availability(
                    result['id'],
                    result['doctor_id'],
                    convert_time.get_start_time_string(result['start']),
                    result['room'],
                    result['free'],
                    result['year'],
                    result['month'],
                    result['day'],
                    result['booking_type']))

        return list_of_availabilities


    def get_availability(self, availability_id):
        """ Queries the Availability db by availability_id and returns an Availability object """

        select_stmt = '''SELECT * FROM Availability
                        WHERE id = ?'''
        params = (availability_id, )

        result = self.db.read_one(select_stmt, params)
        
        if result is None:
            return False

        return Availability(
            result['id'],
            result['doctor_id'],
            convert_time.get_start_time_string(result['start']),
            result['room'],
            result['free'],
            result['year'],
            result['month'],
            result['day'],
            uber_sante.models.scheduler.AppointmentRequestType(result['booking_type']))

    def get_availability_by_doctor_id(self, doctor_id):
        """ Queries the Availability db by availability_id and returns an Availability object """

        select_stmt = '''SELECT * FROM Availability
                        WHERE doctor_id = ?'''
        params = (doctor_id, )

        results = self.db.read_all(select_stmt, params)
        
        if len(results) == 0:
            return AvailabilityStatus.NO_AVAILABILITIES
        
        list_of_availabilities = []

        for result in results:
            list_of_availabilities.append(
                Availability(
                    result['id'],
                    result['doctor_id'],
                    result['start'],
                    result['room'],
                    result['free'],
                    result['year'],
                    result['month'],
                    result['day'],
                    uber_sante.models.scheduler.AppointmentRequestType(result['booking_type'])))

        return list_of_availabilities


    def free_availability(self, availability_id):

        update_stmt = '''UPDATE Availability
                        SET free = 1
                        WHERE id = ?'''
        params = (availability_id, )

        self.db.write_one(update_stmt, params)

        return AvailabilityStatus.SUCESS


    def validate_availability_and_reserve(self, availability_id):

        select_stmt = '''SELECT * FROM Availability
                        WHERE id = ?
                        AND free = 1'''

        update_stmt = '''UPDATE Availability
                        SET free = 0
                        WHERE id = ?'''
        params = (availability_id, )

        result = self.db.read_one(select_stmt, params)

        if result is None:
            return None

        else:
            self.db.write_one(update_stmt, params)

            return Availability(
                result['id'],
                result['doctor_id'],
                result['start'],
                result['room'],
                result['free'],
                result['year'],
                result['month'],
                result['day'],
                uber_sante.models.scheduler.AppointmentRequestType(result['booking_type']))


    def check_and_create_availability_walkin(self, doctor_id, start, room, free, year, month, day, booking_type):
        
        start_time = convert_time.get_time_to_second(start)

        select_stmt = '''SELECT * FROM Availability
                        WHERE start = ?
                        '''
        select_params = (start_time,)
        results = self.db.read_all(select_stmt, select_params)

        if len(results) > 0:
            return AvailabilityStatus.NO_AVAILABILITIES_AT_THIS_HOUR
        
        insert_stmt = '''INSERT INTO Availability(
                            doctor_id,
                            start,
                            room,
                            free,
                            year,
                            month,
                            day,
                            booking_type)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        insert_params = (doctor_id, start_time, room, free, year, month, day, booking_type)

        self.db.write_one(insert_stmt, insert_params)
        return insert_params


    def check_and_create_availability_annual(self, doctor_id, start, room, free, year, month, day, booking_type):
        
        # check the start time, as well as the next 2 slots in the hour
        start_time = convert_time.get_time_to_second(start)
        start_time_plus_20 = convert_time.add_20_minutes(start_time)
        start_time_plus_40 = convert_time.add_20_minutes(start_time_plus_20)

        select_stmt = '''SELECT * FROM Availability
                        WHERE start = ?
                        OR start = ?
                        OR start = ?
                        '''
        select_params = (start_time, start_time_plus_20, start_time_plus_40)
        results = self.db.read_all(select_stmt, select_params)

        if len(results) > 0:
            return AvailabilityStatus.NO_AVAILABILITIES_AT_THIS_HOUR

        insert_stmt = '''INSERT INTO Availability(
                            doctor_id,
                            start,
                            room,
                            free,
                            year,
                            month,
                            day,
                            booking_type)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        insert_params = (doctor_id, start_time, room, free, year, month, day, booking_type)

        self.db.write_one(insert_stmt, insert_params)
        return insert_params

    
    def cancel_availability(self, availability_id):
    
        delete_stmt = '''DELETE FROM Availability
                        WHERE id = ?'''
        params = (availability_id, )

        self.db.write_one(delete_stmt, params)
        return AvailabilityStatus.SUCESS


    def room_is_available_at_this_time(self, start, room, year, month, day):
        """ Checks the Availability table to see if the room is already taken at the given time """
        select_stmt = '''SELECT * FROM Availability WHERE start = ? AND room = ? AND year = ? AND month = ? AND day = ? AND FREE = 1'''
        params = (start, room, year, month, day)

        result = self.db.read_one(select_stmt, params)

        if result is None:
            return AvailabilityStatus.SUCESS

        else:
            return False
