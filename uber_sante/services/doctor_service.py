from uber_sante.utils.dbutil import DBUtil


class DoctorService:

    def __init__(self):
        self.db = DBUtil.get_instance()
