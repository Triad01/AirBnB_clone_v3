#!/usr/bin/python3
""" Module contains set up for flask application"""

from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tear_down(exception):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Returning custom error message """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST")
    if host is None:
        host = '0.0.0.0'

    port = os.getenv("HBNB_API_PORT")
    if port is None:
        port = '5000'
    app.run(debug=True, host=host, port=port, threaded=True)
