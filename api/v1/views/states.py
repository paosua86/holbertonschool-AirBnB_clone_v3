#!/usr/bin/python3
"""Create a new VIEW for State objects that
handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State

# You must use to_dict() to retrieve an object into a valid JSON

@app_views.route("/states", methods=['GET'])
def get_states():
    """retrieves states"""
    list = []
    for state in storage.all(State).values():
        list.append(state.to_dict())
    return jsonify(list)


# Retrieves a State object: GET /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['GET'])
def states_by_id(state_id):
    """retrieves the state"""
    for state in storage.all(State).values():
        if state.id == state_id:
            return jsonify(state.to_dict())
# If the state_id is not linked to any State object, raise a 404 error
    abort(404)


# Deletes a State object:: DELETE /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_states(state_id):
    """deletes a state"""
    if not storage.get(State, state_id):
# If the state_id is not linked to any State object, raise a 404 error
        abort(404)
    State.delete()
    storage.save()
# Returns an empty dictionary with the status code 200
    return jsonify({}), 200


# Creates a State: POST /api/v1/states
@app_views.route('/states', methods=['POST'])
def states_post(state_id):
    """You must use request.get_json from Flask to transform the HTTP body request to a dictionary"""
# If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
    if not request.get_json():
        abort(400, "Not a JSON")
# If the dictionary doesn't contain the key name, raise a 400 error with the message Missing name
    if 'name' not in request.get_json().keys():
        abort(400, "Missing name")
# Returns the new State with the status code 201
    new_state = State(**request.get_json())
    new_state.save()
    return jsonify(new_state.to_dict()), 201


# Updates a State object: PUT /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['PUT'])
def states_put(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
# If the state_id is not linked to any State object, raise a 404 error
    if not state:
        abort(404)
# You must use request.get_json from Flask to transform the HTTP body request to a dictionary
# If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
    if not request.get_json():
        abort(400, "Not a JSON")
# Update the State object with all key-value pairs of the dictionary
    for key, value in request.get_json().items():
# # Ignore keys: id, created_at and updated_at
        if key in ["id", "created_at", "updated_at"]:
            continue
        else:
            setattr(state, key, value)
# Returns the State object with the status code 200
    storage.save()
    return jsonify(state.to_dict()), 200







