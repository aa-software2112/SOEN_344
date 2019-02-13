import os
from flask import Flask
from config import Config
from uber_sante.utils.dbutil import DBUtil

app = Flask('uber_sante')
app.config.from_object(__name__)

app.config.from_object(Config)

db_util = DBUtil(app)
db = DBUtil.get_instance(db_util)