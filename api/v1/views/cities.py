#!/usr/bin/python3
"""create a new view for City objects that handles
all default RESTFul API actions"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


# You must use to_dict() to retrieve an object into a valid JSON
# Retrieves the list of all City objects of a State: GET
# /api/v1/states/<state_id>/cities
@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def get_cities(state_id):
    """retrieves cities"""
    state = storage.get(State, state_id)
    # If the state_id is not linked to any State object, raise a 404 error
    if not state:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


# Retrieves a City object. : GET /api/v1/cities/<city_id>
@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def cities_by_id(city_id):
    """retrieves the state"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
# If the state_id is not linked to any State object, raise a 404 error
    abort(404)


# Deletes a City object: DELETE /api/v1/cities/<city_id>
@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_cities(city_id):
    """deletes a state"""
    city = storage.get(City, city_id)
    if not city:
        # If the city_id is not linked to any City object,
        # raise a 404 error
        abort(404)
    city.delete()
    storage.save()
    # Returns an empty dictionary with the status code 200
    return jsonify({}), 200


# Creates a City: POST /api/v1/states/<state_id>/cities
@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def cities_post(state_id):
    """You must use request.get_json from Flask to
    transform the HTTP body request to a dictionary"""
    # If the HTTP body request is not valid JSON, raise a 400 error
    # with the message Not a JSON
    if not request.get_json():
        abort(400, "Not a JSON")
    # If the state_id is not linked to any State object, raise a 404 error
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    # If the dictionary doesn't contain the key name, raise
    # a 400 error with the message Missing name
    if 'name' not in request.get_json().keys():
        abort(400, "Missing name")
    # Returns the new City with the status code 201
    new_city = City(**request.get_json())
    setattr(new_city, 'state_id', state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


# Updates a City object: PUT /api/v1/cities/<city_id>
@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def cities_put(city_id):
    """Updates a State object"""
    city = storage.get(City, city_id)
    # If the city_id is not linked to any City object, raise a 404 error
    if not city:
        abort(404)
    # You must use request.get_json from Flask to transform the HTTP body
    # request to a dictionary
    # If the HTTP body request is not valid JSON, raise a 400 error
    # with the message Not a JSON
    if not request.get_json():
        abort(400, "Not a JSON")
    # Update the City object with all key-value pairs of the dictionary
    for key, value in request.get_json().items():
        # Ignore keys: id, state_id, created_at and updated_at
        if key in ["id", "state_id", "created_at", "updated_at"]:
            continue
        else:
            setattr(city, key, value)
    # Returns the City object with the status code 200
    storage.save()
    return jsonify(city.to_dict()), 200
