import os
import sqlite3
from uber_sante.utils.config import DB_CONFIG


class DBUtil:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if DBUtil.__instance is None:
            DBUtil.__instance = DBUtil()
        return DBUtil.__instance

    def __init__(self):

        if DBUtil.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.__instance = self
            self.__init_database()

    def __init_database(self):
        """ Creates and populates the database if it does not already exit """
        if not os.path.isfile(DB_CONFIG['path_to_db']):
            print(' * No database found; creating and populating one... ')
            print(DB_CONFIG['path_to_db'])
            rv = sqlite3.connect(DB_CONFIG['path_to_db'])

            with open(DB_CONFIG['path_to_script']) as file:
                rv.cursor().executescript(file.read())

    def reset_database(self):
        os.remove(DB_CONFIG['path_to_db'])
        self.__init_database()

    def __connect(self):

        rv = sqlite3.connect(DB_CONFIG['path_to_db'])
        rv.row_factory = create_dictionary
        return rv

    def read_one(self, query, params):
        """ Performs a read (select) query and returns the first result """
        rv = self.__connect()
        cursor = rv.cursor()
        cursor.execute(query, params)
        value = cursor.fetchone()
        rv.close()
        return value

    def read_all(self, query, params):
        """ Performs a read (select) query and returns all the results """
        rv = self.__connect()
        cursor = rv.cursor()
        cursor.execute(query, params)
        values = cursor.fetchall()
        rv.close()
        return values

    def write_one(self, query, params):
        """ Performs one write (insert, delete, update) query """
        rv = self.__connect()
        cursor = rv.cursor()
        cursor.execute(query, params)
        rv.commit()
        rv.close()

    def write_many(self, queries, params):
        """ Performs multiple write (insert, delete, update) queries in the same session (Unit of Work) """
        rv = self.__connect()
        cursor = rv.cursor()
        for i in range(0, len(queries)):
            cursor.execute(queries[i], params[i])
        rv.commit()
        rv.close()


def create_dictionary(cursor, row):

    result = {}
    for idx, col in enumerate(cursor.description):
        result[col[0]] = row[idx]
    return result
