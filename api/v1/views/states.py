#!/usr/bin/python3
"""module for creating state crud"""
from models import storage
from flask import jsonify, abort, request
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def getAllStates():
    """get all states"""
    states_store = []
    all_states = storage.all("State")
    for obj in all_states.values():
        states_store.append(obj.to_dict())
    return jsonify(states_store)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_states_byid(state_id):
    """get states by id"""
    get_by_id = storage.get("State", state_id)
    if get_by_id is None:
        abort(404)
    return jsonify(get_by_id.to_dict())


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """create new state"""
    state_json = request.get_json(silent=True)
    if not state_json:
        abort(400, 'Not a JSON')
    if 'name' not in state_json:
        abort(400, 'Missing name')

    created_state = State(**state_json)
    created_state.save()
    response = jsonify(created_state.to_dict())
    response.status_code = 201
    return response


@app_views.route(
        "/states/<state_id>", methods=['DELETE'], strict_slashes=False
        )
def delete_state(state_id):
    """delete states by id"""
    get_by_id = storage.get("State", state_id)
    if get_by_id is None:
        abort(404)
    storage.delete(get_by_id)
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update the state"""
    get_by_id = storage.get("State", state_id)
    if get_by_id is None:
        abort(404)

    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(get_by_id, key, val)
    get_by_id.save()
    return jsonify(get_by_id.to_dict())
