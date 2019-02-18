from flask import Flask, request, jsonify
from uber_sante.utils.dbutil import DBUtil
from uber_sante.controllers import controllers

app = Flask(__name__)

db = DBUtil.get_instance()

app.register_blueprint(controllers)  # always register blueprints after 'app' routes


# Can use this for print testing/debugging
@app.route('/test', methods=["GET"])
def test():
    if request.method == 'GET':

        query = 'SELECT * FROM Patient'
        results = []
        for row in db.read_all(query, ()):
            results.append(row)

        return jsonify(results), 200
