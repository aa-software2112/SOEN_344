import os
import sqlite3
from app import app
from config import Config
from app.controllers import controllers
from app.utils.dbutil import DBUtil
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
    
app = Flask('app')
app.config.from_object(__name__)

Config.DATABASE = os.path.join(app.root_path + '/db/', 'database.db')
app.config.from_object(Config)

db = DBUtil(app, True).get_instance(False)

@app.route('/')
def welcome_message(): 
    return 'Hello world'

@app.route('/hi', methods=["GET"])
def test():
    if request.method == 'GET':
        query = 'SELECT * FROM Patient'
        results = []
        for row in db.return_all(query, ()):
            results.append(row)

        return jsonify(results), 200

app.register_blueprint(controllers) # always register blueprints after 'app' routes

if __name__ == "__main__":
    app.run(debug=True)
