import uuid

class booking:

    def __init__(self, avail_id, doc_id, pat_id):
        self.id = uuid.uuid4()
        self.availability_id = avail_id
        self.doctor_id = doc_id
        self.patient_id = pat_id

