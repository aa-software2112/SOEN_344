from enum import Enum

from uber_sante.models.clinic import Clinic

from uber_sante.utils.dbutil import DBUtil
from uber_sante.utils.time_interpreter import TimeInterpreter

convert_time = TimeInterpreter()

class ClinicStatus(Enum):
    SUCESS = 1
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
                    convert_time.get_start_time_string(result['close_time'])))
                    
        list_of_clinics.sort(key=lambda x: x.location, reverse=False)
        return list_of_clinics
    
    def modify_clinic(self, id, name, location, nb_rooms, nb_doctors, nb_nurses, open_time, close_time):
        update_stmt = '''UPDATE Clinic
                        SET
                            name = ?,
                            location = ?,
                            nb_rooms = ?,
                            nb_doctors = ?,
                            nb_nurses = ?,
                            open_time = ?,
                            close_time = ?,
                        WHERE id = ?'''
        params = (id, name , location, nb_rooms, nb_doctors, nb_nurses, open_time, close_time)

        self.db.write_one(update_stmt, params)

        return ClinicStatus.SUCCESS
