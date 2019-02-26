from enum import Enum

from uber_sante.utils.dbutil import DBUtil

class AdminService:

    def __init__(self):
        self.db = DBUtil.get_instance()

    def validate_login_info(self, email, password):

        select_stmt = 'SELECT id, password FROM Admin WHERE email = ?'
        params = (email,)

        result = self.db.read_one(select_stmt, params)

        # Incorrect email
        if result is None:
            return -1

        # Incorrect password
        if password != result['password']:
            return -1

        return result['id']

