import os
import sqlite3

class DBUtil:

    instance = None
    app = None

    def __init__(self, app, test=False):
        if DBUtil.instance is None:
            DBUtil.instance = self
            self.app = app
            self.test = test
            self.init_database()
            self.connect_db = self.connect_database
    
    def get_instance(self):
        if self.instance is None:
            self.instance = DBUtil(self.app)
        return self.instance

    def init_database(self):
        print(self.app.config['DATABASE'])
        if os.path.isfile(self.app.config['DATABASE']):
            os.remove(self.app.config['DATABASE'])

        rv = sqlite3.connect(self.app.config['DATABASE'])
        rv.row_factory = create_dictionary
        with self.app.open_resource('db/database.sql', mode='r') as f:
            rv.cursor().executescript(f.read())
        rv.commit()
        return rv

    def connect_database(self):
        rv = sqlite3.connect(self.app.config['DATABASE']) 
        rv.row_factory = create_dictionary
        return rv

    def init_test_database(self):
        if os.path.isfile('db/database_test.db'):
            os.remove('database_test.db')

        rv = sqlite3.connect('database_test.db')
        rv.row_factory = create_dictionary
        with self.app.open_resource('db/database.sql', mode='r') as f:
            rv.cursor().executescript(f.read())
        rv.commit()
        return rv
    
    def connect_test_database(self):
        rv = sqlite3.connect('app/db/test_database.db')
        rv.row_factory = create_dictionary
        return rv

    def return_single(self, query, params):
        rv = self.connect_db()
        cursor = rv.cursor()
        cursor.execute(query, params)
        value = cursor.fetchone()
        rv.close()
        return value
        
    def return_all(self, query, params):
        rv = self.connect_db()
        cursor = rv.cursor()
        cursor.execute(query, params)
        values = cursor.fetchall()
        rv.close()
        return values

    def return_none(self, queries, params):
        rv = self.connect_db()
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
