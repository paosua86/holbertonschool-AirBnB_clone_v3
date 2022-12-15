#!/usr/bin/python3
"""Create a new VIEW for place objects that
handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


# Retrieves the list of all Place objects of a City: GET /api/v1/cities/<city_id>/places
@app_views.route("/cities/<city_id>/places", strict_slashes=False, methods=['GET'])
def get_places_by_city(city_id):
    city = storage.get(City, city_id)
    # If the city_id is not linked to any City object
    # raise a 404 error
    if not city:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)

@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])


# Retrieves a Place object. : GET /api/v1/places/<place_id>
@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def places_by_id(place_id):
    """retrieves the places"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
# If the place_id is not linked to any Place object, raise a 404 error
    abort(404)


# Deletes a Place object: DELETE /api/v1/places/<place_id>
@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """deletes a Amenity"""
    place = storage.get(Place, place_id)
    if not place:
        # If the place_id is not linked to any Place object
        # raise a 404 error
        abort(404)
    place.delete()
    storage.save()
    # Returns an empty dictionary with the status code 200
    return jsonify({}), 200


# Creates a Place: POST /api/v1/cities/<city_id>/places
@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def places_post(city_id):
    """You must use request.get_json from Flask to
    transform the HTTP body request to a dictionary"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    # If the HTTP body request is not valid JSON, raise a 400 error
    # with the message Not a JSON
    if not request.get_json():
        abort(400, "Not a JSON")
    # If the dictionary doesn't contain the key name, raise
    # a 400 error with the message Missing name
    if 'user_id' not in request.get_json().keys():
        abort(400, "Missing user_id")
    # If the dictionary doesn’t contain the key name, raise a
    # 400 error with the message Missing name
    if 'name' not in request.get_json().keys():
        abort(400, "Missing name")
    # If the user_id is not linked to any User object, raise a 404 error
    valid_user = storage.get(User, request.get_json()['user_id'])
    if not valid_user:
        abort(404)
    # Returns the new Amenity with the status code 201
    new_place = Place(**request.get_json())
    setattr(new_place, 'city_id', city_id)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


# Updates a Place object: PUT /api/v1/places/<place_id>
@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def places_put(place_id):
    """Updates a place object"""
    place = storage.get(Place, place_id)
    # If the place_id is not linked to any place object, raise a 404 error
    if not place:
        abort(404)
    # You must use request.get_json from Flask to transform the HTTP body
    # request to a dictionary
    # If the HTTP body request is not valid JSON, raise a 400 error
    # with the message Not a JSON
    if not request.get_json():
        abort(400, "Not a JSON")
    # Update the place object with all key-value pairs of the dictionary
    for key, value in request.get_json().items():
        # Ignore keys: id, user_id, city_id, created_at and updated_at
        if key in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            continue
        else:
            setattr(place, key, value)
    # Returns the place object with the status code 200
    storage.save()
    return jsonify(place.to_dict()), 200
