#!/usr/bin/python3
"""index file of our flask application"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    amenities = storage.count(classes.get('Amenity'))
    cities = storage.count(classes.get('City'))
    places = storage.count(classes.get('Place'))
    reviews = storage.count(classes.get('Review'))
    states = storage.count(classes.get('State'))
    users = storage.count(classes.get('User'))
    return jsonify({
                    "amenities": amenities,
                    "cities": cities,
                    "places": places,
                    "reviews": reviews,
                    "states": states,
                    "users": users})
