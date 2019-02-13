import os
from flask import Flask
from config import Config
from uber_sante.utils.dbutil import DBUtil

app = Flask('uber_sante')
app.config.from_object(__name__)

Config.DATABASE = os.path.join(app.root_path + '/db/', 'database.db')
app.config.from_object(Config)

db_util = DBUtil(app, False)
db = DBUtil.get_instance(db_util)