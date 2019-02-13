import uuid

class availability:

    def __init__(self, doctor_id, start, end, room):
        self.id = uuid.uuid4()
        self.doctor_id = doctor_id
        self.start = start
        self.end = end
        self.room = room
