from enum import Enum

from uber_sante.models.clinic import Clinic

from uber_sante.utils.dbutil import DBUtil
from uber_sante.utils.time_interpreter import TimeInterpreter

convert_time = TimeInterpreter()


class ClinicStatus(Enum):
    SUCCESS = 1
    CLINIC_DOES_NOT_EXIST = -1


class ClinicService:

    def __init__(self):
        self.db = DBUtil.get_instance()

    def get_clinics(self):
        select_stmt = '''SELECT * FROM Clinic'''
        params = ()

        results = self.db.read_all(select_stmt, params)

        list_of_clinics = []

        for result in results:
            list_of_clinics.append(
                Clinic(
                    result['id'],
                    result['name'],
                    result['location'],
                    result['nb_rooms'],
                    result['nb_doctors'],
                    result['nb_nurses'],
                    convert_time.get_start_time_string(result['open_time']),
                    convert_time.get_start_time_string(result['close_time']),
                    result['phone']))

        list_of_clinics.sort(key=lambda x: x.location, reverse=False)
        return list_of_clinics

    def get_current_clinic(self, user_type, id):

        if user_type == "patient":
            select_stmt = '''SELECT clinic_id FROM Patient WHERE id = ?'''
        elif user_type == "doctor":
            select_stmt = '''SELECT clinic_id FROM Doctor WHERE id = ?'''
        elif user_type == "nurse":
            select_stmt = '''SELECT clinic_id FROM Nurse WHERE id = ?'''
        else:
            return None

        params = (id,)

        clinic = self.db.read_all(select_stmt, params)
        clinic_id = clinic[0]['clinic_id']

        select_stmt = '''SELECT * FROM Clinic WHERE id = ?'''
        params = (str(clinic_id))

        result = self.db.read_all(select_stmt, params)

        return result


    def register_clinic(self, name, location, nb_rooms, nb_doctors, nb_nurses, open_time, close_time, phone):
        update_stmt = '''INSERT INTO Clinic(
                                name,
                                location,
                                nb_rooms,
                                nb_doctors,
                                nb_nurses,
                                open_time,
                                close_time,
                                phone)
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?)'''
        params = (name, location, nb_rooms, nb_doctors, nb_nurses, open_time, close_time, phone)

        self.db.write_one(update_stmt, params)

        return ClinicStatus.SUCCESS

    def modify_clinic(self, id, name, location, nb_rooms, nb_doctors, nb_nurses, open_time, close_time, phone):
        update_stmt = '''UPDATE Clinic
                            SET
                                name = ?,
                                location = ?,
                                nb_rooms = ?,
                                nb_doctors = ?,
                                nb_nurses = ?,
                                open_time = ?,
                                close_time = ?,
                                phone = ?,
                            WHERE id = ?'''
        params = (id, name, location, nb_rooms, nb_doctors, nb_nurses, open_time, close_time, phone)

        self.db.write_one(update_stmt, params)

        return ClinicStatus.SUCCESS
    
    def modify_clinic_limited(self, id, location, open_time, close_time, phone):

        select_stmt = '''SELECT * FROM Clinic WHERE id = ?'''
        params = (id,)

        results = self.db.read_all(select_stmt, params)

        list_of_clinics = []

        for result in results:
            list_of_clinics.append(
                Clinic(
                    result['id'],
                    result['name'],
                    result['location'],
                    result['nb_rooms'],
                    result['nb_doctors'],
                    result['nb_nurses'],
                    convert_time.get_start_time_string(result['open_time']),
                    convert_time.get_start_time_string(result['close_time']),
                    result['phone']))

        if (len(list_of_clinics) > 0):
            name = list_of_clinics[0].name
            nb_rooms = list_of_clinics[0].nb_rooms
            nb_doctors = list_of_clinics[0].nb_doctors
            nb_nurses = list_of_clinics[0].nb_nurses

            delete_stmt = '''DELETE FROM Clinic
                            WHERE id = ?'''
            params = (id,)

            self.db.write_one(delete_stmt, params)

            insert_stmt = '''INSERT INTO Clinic(
                                    id,
                                    name,
                                    location,
                                    nb_rooms,
                                    nb_doctors,
                                    nb_nurses,
                                    open_time,
                                    close_time,
                                    phone)
                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            params = (id, name, location, nb_rooms, nb_doctors, nb_nurses, open_time, close_time, phone)

            self.db.write_one(insert_stmt, params)

            return ClinicStatus.SUCCESS
        else:
            return ClinicStatus.CLINIC_DOES_NOT_EXIST
