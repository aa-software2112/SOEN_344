class Booking(object):

    def __init__(self, booking_id, avail_id, doc_id, pat_id):
        self.id = booking_id
        self.availability_id = avail_id
        self.doctor_id = doc_id
        self.patient_id = pat_id
