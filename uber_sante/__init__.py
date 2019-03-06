from flask import Flask, request, jsonify
from uber_sante.utils.dbutil import DBUtil
from uber_sante.controllers import controllers
from uber_sante.utils import json_helper as js
from flask_cors import CORS

app = Flask(__name__)

db = DBUtil.get_instance()

app.register_blueprint(controllers)  # always register blueprints after 'app' routes
CORS(app, resources={r"/*": {"origins": "*"}})


@app.before_request
def respond_to_options_request():

    if request.method == "OPTIONS":
        return js.create_json(data=None, message=None, return_code=js.ResponseReturnCode.CODE_200)


# Can use this for print testing/debugging
@app.route('/test', methods=["GET"])
def test():
    if request.method == 'GET':

        query = 'SELECT * FROM Patient'
        results = []
        for row in db.read_all(query, ()):
            results.append(row)

        return jsonify(results), 200

