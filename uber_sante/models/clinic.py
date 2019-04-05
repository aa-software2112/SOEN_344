class Clinic:

    def __init__(self, clinic_id, name, location, nb_rooms, nb_doctors, nb_nurses, open_time, close_time, phone):
        self.id = clinic_id
        self.name = name
        self.location = location
        self.nb_rooms = nb_rooms
        self.nb_doctors = nb_doctors
        self.nb_nurses = nb_nurses
        self.open_time = open_time      #in seconds from start of day
        self.close_time = close_time    #in seconds from start of day
        self.phone = phone

    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'nb_rooms': self.nb_rooms,
            'nb_doctors': self.nb_doctors,
            'nb_nurses': self.nb_nurses,
            'open_time': self.open_time,
            'close_time': self.close_time,
            'phone': self.phone
        }