import os
from flask import Flask 

app = Flask('uber_sante')

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE = os.path.join(app.root_path + '/db/', 'database.db')
    SECRET_KEY='jeinx2903jnfkknd29102jsn'
    USERNAME='admin'
    PASSWORD='bigboat123'
