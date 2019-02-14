from uber_sante import app, db
from uber_sante.controllers import controllers
from flask import Flask, request, jsonify

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
