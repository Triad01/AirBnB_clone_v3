#!/usr/bin/python3
"""index file of our flask application"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """shows the status of our application"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """ retrieves the number of each objects by type """
    class_dict = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    objs = {class_dict[cls]: storage.count(cls) for cls in class_dict}
    return jsonify(objs)
