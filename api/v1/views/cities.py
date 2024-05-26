#!/usr/bin/python3
""" Modlule shows CRUD implementation for City model"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """ Retrieves a list of cities for a state

        Args:
            state_id (str): The UUID4 string representing a State object

        Returns:
            list of dictionaries representing city objects in JSON format
    """
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    cities = [city.to_dict() for city in state_obj.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a city by its id

        Args:
            city_id: UUID4 string represending a city object

        Return: Dictionary representation of a city object
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city by its id

        Args:
            city_id: UUID4 representation of a city object

        Returns: an empty dicitionary indicating successful obj delection
    """
    city_obj = storage.get("City", city_id)
    city_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a city object using state id

        Args:
            state_id: UUID4 representation of a state object

        Returns: the newly created city object with a 201 status code
    """
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    request_fields = request.get_json()
    if request_fields.get('name') is None:
        return "Missing name", 400
    request_fields['state_id'] = state_id
    new_city = City(**request_fields)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ Updates a city object by its id

        Args:
            city_id: UUID4 representation of a city object

        Returns: an updated dictionary of the city object
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    request_fields = request.get_json()
    for key in request_fields:
        if key in ["id", "state_id", "created_at", "updated_at"]:
            continue
        if hasattr(city_obj, key):
            setattr(city_obj, key, request_fields[key])  # actual update
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
