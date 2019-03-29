class Clinic:

    def __init__(self, clinic_id, name, location, nb_rooms, nb_doctors, nb_nurses, open_time, close_time):
        self.id = clinic_id
        self.name = name
        self.location = location
        self.nb_rooms = nb_rooms
        self.nb_doctors = nb_doctors
        self.nb_nurses = nb_nurses
        self.open_time = open_time      #in seconds from start of day
        self.close_time = close_time    #in seconds from start of day