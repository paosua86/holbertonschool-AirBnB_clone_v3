#!/usr/bin/python3
"""Create a new VIEW for Amenity objects that
handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity


# You must use to_dict() to retrieve an object into a valid JSON
@app_views.route("/amenities", strict_slashes=False, methods=['GET'])
def get_amenities():
    """retrieves Amenitys"""
    list = []
    for amenity in storage.all(Amenity).values():
        list.append(amenity.to_dict())
    return jsonify(list)


# Retrieves a Amenity object: GET /api/v1/Amenitys/<Amenity_id>
@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def amenitys_by_id(amenity_id):
    """retrieves the Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
# If the Amenity_id is not linked to any Amenity object, raise a 404 error
    abort(404)


# Deletes a Amenity object:: DELETE /api/v1/Amenitys/<Amenity_id>
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenities(amenity_id):
    """deletes a Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        # If the Amenity_id is not linked to any Amenity object,
        # raise a 404 error
        abort(404)
    amenity.delete()
    storage.save()
    # Returns an empty dictionary with the status code 200
    return jsonify({}), 200


# Creates a Amenity: POST /api/v1/Amenitys
@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def Amenitys_post():
    """You must use request.get_json from Flask to
    transform the HTTP body request to a dictionary"""
    # If the HTTP body request is not valid JSON, raise a 400 error
    # with the message Not a JSON
    if not request.get_json():
        abort(400, "Not a JSON")
    # If the dictionary doesn't contain the key name, raise
    # a 400 error with the message Missing name
    if 'name' not in request.get_json().keys():
        abort(400, "Missing name")
    # Returns the new Amenity with the status code 201
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


# Updates a Amenity object: PUT /api/v1/Amenitys/<Amenity_id>
@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def Amenitys_put(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    # If the Amenity_id is not linked to any Amenity object, raise a 404 error
    if not amenity:
        abort(404)
    # You must use request.get_json from Flask to transform the HTTP body
    # request to a dictionary
    # If the HTTP body request is not valid JSON, raise a 400 error
    # with the message Not a JSON
    if not request.get_json():
        abort(400, "Not a JSON")
    # Update the Amenity object with all key-value pairs of the dictionary
    for key, value in request.get_json().items():
        # Ignore keys: id, created_at and updated_at
        if key in ["id", "created_at", "updated_at"]:
            continue
        else:
            setattr(amenity, key, value)
    # Returns the Amenity object with the status code 200
    storage.save()
    return jsonify(amenity.to_dict()), 200
