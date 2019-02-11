import os
import sqlite3
from app import app
from app.utils.dbutil import DBUtil

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
    
app = Flask('app')
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path + '/app/db/', 'database.db'),
    SECRET_KEY='jeinx2903jnfkknd29102jsn',
    USERNAME='admin',
    PASSWORD='bigboat123'
))

app.config.from_envvar('UBERSANTE_SETTINGS', silent=True)
db = DBUtil(app, True)


@app.route('/')
def welcome_message(): 
    return 'Hello world'

# CRUD operations on product
@app.route('/hi', methods=["GET"])
def test():
    if request.method == 'GET':
        query = 'SELECT * FROM Patient'
        results = []
        for row in db.return_all(query, ()):
            results.append(row)
            
        return jsonify(results), 200

if __name__ == "__main__":
    app.run(debug=True)
