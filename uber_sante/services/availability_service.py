import uber_sante
from enum import Enum

from uber_sante.models.availability import Availability

from uber_sante.utils.dbutil import DBUtil
from uber_sante.utils.time_interpreter import TimeInterpreter

convert_time = TimeInterpreter()


class AvailabilityStatus(Enum):
    SUCCESS = 1
    NO_AVAILABILITIES = 2
    NO_ROOMS_AT_THIS_TIME = 3
    AVAILABILITY_ALREADY_BOOKED_AT_THIS_TIME = 4  # doctor has already booked an availability at this time slot
    ALL_ROOMS_OPEN = 5


class AvailabilityService:

    def __init__(self):
        self.db = DBUtil.get_instance()

    def get_availabilities(self, schedule_request, clinic_id):
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
                            AND free = 1
                            AND (? = "ALL" OR booking_type = ?) 
                            AND clinic_id = ?'''
            params = (year, month, day, appointment_request_type, appointment_request_type, clinic_id)

        elif schedule_request.is_monthly_request():

            # If the booking_type is BookingType.ALL (which has value ""), it will select all rows
            select_stmt = '''SELECT * FROM Availability
                          WHERE year = ?
                          AND month = ?
                          AND free = 1
                          AND (? = "ALL" OR booking_type = ?) 
                          AND clinic_id = ?'''
            params = (year, month, appointment_request_type, appointment_request_type, clinic_id)

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
                    result['booking_type'],
                    result['clinic_id']))

        return list_of_availabilities

    def get_availability(self, availability_id):
        """ Queries the Availability db by availability_id and returns an Availability object """

        select_stmt = '''SELECT * FROM Availability
                        WHERE id = ?'''
        params = (availability_id,)

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
            uber_sante.models.scheduler.AppointmentRequestType(result['booking_type']),
            result['clinic_id'])

    def get_all_availabilities(self):

        select_stmt = '''SELECT * FROM Availability'''
        params = ()
        results = self.db.read_all(select_stmt, params)

        if len(results) == 0:
            return AvailabilityStatus.NO_AVAILABILITIES

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
                    uber_sante.models.scheduler.AppointmentRequestType(result['booking_type']),
                    result['clinic_id']))

        return list_of_availabilities

    def get_available_rooms(self, start, year, month, day):

        start_time = convert_time.get_time_to_second(start)

        select_stmt = '''SELECT * FROM Availability
                        WHERE start = ?
                        AND year = ?
                        AND month = ?
                        AND day = ?'''
        params = (start_time, year, month, day)

        results = self.db.read_all(select_stmt, params)

        if len(results) == 0:
            return AvailabilityStatus.ALL_ROOMS_OPEN
        if len(results) == 5:
            return AvailabilityStatus.NO_ROOMS_AT_THIS_TIME

        list_of_availabilities = []

        for result in results:
            list_of_availabilities.append({'room': result['room']})

        return list_of_availabilities

    def get_availability_by_doctor_id(self, doctor_id):
        """ Queries the Availability db by availability_id and returns an Availability object """

        select_stmt = '''SELECT * FROM Availability
                        WHERE doctor_id = ?'''
        params = (doctor_id,)

        results = self.db.read_all(select_stmt, params)

        if len(results) == 0:
            return AvailabilityStatus.NO_AVAILABILITIES

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
                    uber_sante.models.scheduler.AppointmentRequestType(result['booking_type']),
                    result['clinic_id']))

        return list_of_availabilities

    def free_availability(self, availability_id):

        update_stmt = '''UPDATE Availability
                        SET free = 1
                        WHERE id = ?'''
        params = (availability_id,)

        self.db.write_one(update_stmt, params)

        return AvailabilityStatus.SUCCESS

    def validate_availability_and_reserve(self, availability_id):

        select_stmt = '''SELECT * FROM Availability
                        WHERE id = ?
                        AND free = 1'''

        update_stmt = '''UPDATE Availability
                        SET free = 0
                        WHERE id = ?'''
        params = (availability_id,)

        result = self.db.read_one(select_stmt, params)

        if result is None:
            print("Cannot validate availability.")
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
                uber_sante.models.scheduler.AppointmentRequestType(result['booking_type']),
                result['clinic_id'])

    def check_and_create_availability_walkin(self, doctor_id, start, room, free, year, month, day, booking_type, clinic_id,
                                             availability_id=-1):

        if self.check_doctor_time_slot(doctor_id, start, year, month,
                                       day) == AvailabilityStatus.AVAILABILITY_ALREADY_BOOKED_AT_THIS_TIME:
            return AvailabilityStatus.AVAILABILITY_ALREADY_BOOKED_AT_THIS_TIME

        start_time = convert_time.get_time_to_second(start)
        select_stmt = None

        if availability_id != -1:
            select_stmt = '''SELECT * FROM Availability
                            WHERE start = ?
                            AND room = ?
                            AND NOT id = ?'''
            select_params = (start_time, room, availability_id)
        else:
            select_stmt = '''SELECT * FROM Availability
                            WHERE start = ?
                            AND room = ?'''
            select_params = (start_time, room)

        results = self.db.read_all(select_stmt, select_params)

        if len(results) > 0:
            return AvailabilityStatus.NO_ROOMS_AT_THIS_TIME

        insert_stmt = '''INSERT INTO Availability(
                            doctor_id,
                            start,
                            room,
                            free,
                            year,
                            month,
                            day,
                            booking_type, 
                            clinic_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        insert_params = (doctor_id, start_time, room, free, year, month, day, booking_type, clinic_id)

        self.db.write_one(insert_stmt, insert_params)
        return insert_params

    def check_and_create_availability_annual(self, doctor_id, start, room, free, year, month, day, booking_type, clinic_id,
                                             availability_id=-1):

        # check the start time, as well as the next 2 slots in the hour
        start_time = convert_time.get_time_to_second(start)

        start_time_plus_20 = convert_time.add_20_minutes(start_time)
        start_time_plus_40 = convert_time.add_20_minutes(start_time_plus_20)

        select_stmt = None

        if availability_id != -1:
            select_stmt = '''SELECT * FROM Availability
                            WHERE NOT id = ?
                            AND room = ?
                            AND (start = ? OR start = ? OR start = ?)'''
            select_params = (availability_id, room, start_time, start_time_plus_20, start_time_plus_40)
        else:
            select_stmt = '''SELECT * FROM Availability
                            WHERE room = ?
                            AND (start = ? OR start = ? OR start = ?)'''
            select_params = (room, start_time, start_time_plus_20, start_time_plus_40)

        results = self.db.read_all(select_stmt, select_params)

        if len(results) > 0:
            return AvailabilityStatus.NO_ROOMS_AT_THIS_TIME

        insert_stmt = '''INSERT INTO Availability(
                            doctor_id,
                            start,
                            room,
                            free,
                            year,
                            month,
                            day,
                            booking_type,
                            clinic_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        insert_params = (doctor_id, start_time, room, free, year, month, day, booking_type, clinic_id)

        self.db.write_one(insert_stmt, insert_params)
        return insert_params

    def cancel_availability(self, availability_id):

        delete_stmt = '''DELETE FROM Availability
                        WHERE id = ?'''
        params = (availability_id,)

        self.db.write_one(delete_stmt, params)
        return AvailabilityStatus.SUCCESS

    def room_is_available_at_this_time(self, availability_id, start, room, year, month, day):
        """ Checks the Availability table to see if the room is already taken at the given time """
        select_stmt = '''SELECT * FROM Availability
                        WHERE start = ?
                        AND room = ?
                        AND year = ?
                        AND month = ?
                        AND day = ?
                        AND NOT id = ?'''
        params = (start, room, year, month, day, availability_id)
        result = self.db.read_one(select_stmt, params)

        if result is None:
            return AvailabilityStatus.SUCCESS

        else:
            return AvailabilityStatus.NO_ROOMS_AT_THIS_TIME

    def check_doctor_time_slot(self, doctor_id, start, year, month, day):
        """Checks if the doctor is about to book 2 availabilities at the same time slot in different rooms"""
        start_time = convert_time.get_time_to_second(start)

        select_stmt = '''SELECT * FROM Availability
                        WHERE doctor_id = ?
                        AND start = ?
                        AND year = ?
                        AND month = ?
                        AND day = ?'''
        params = (doctor_id, start_time, year, month, day)

        result = self.db.read_one(select_stmt, params)

        if result is None:
            return AvailabilityStatus.SUCCESS
        else:
            return AvailabilityStatus.AVAILABILITY_ALREADY_BOOKED_AT_THIS_TIME
