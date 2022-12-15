#!/usr/bin/python3
"""Create a new VIEW for User objects that
handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User


# You must use to_dict() to retrieve an object into a valid JSON
@app_views.route("/users", strict_slashes=False, methods=['GET'])
def get_users():
    """retrieves Users"""
    list = []
    for user in storage.all(User).values():
        list.append(user.to_dict())
    return jsonify(list)


# Retrieves a users object: GET /api/v1/users/<user_id>
@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def users_by_id(user_id):
    """retrieves the users"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
# If the user_id is not linked to any user object, raise a 404 error
    abort(404)


# Deletes a user object:: DELETE /api/v1/users/<user_id>
@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """deletes a Amenity"""
    user = storage.get(User, user_id)
    if not user:
        # If the user_id is not linked to any User object,
        # raise a 404 error
        abort(404)
    user.delete()
    storage.save()
    # Returns an empty dictionary with the status code 200
    return jsonify({}), 200


# Creates a User: POST /api/v1/users
@app_views.route('/users', strict_slashes=False, methods=['POST'])
def users_post():
    """You must use request.get_json from Flask to
    transform the HTTP body request to a dictionary"""
    # If the HTTP body request is not valid JSON, raise a 400 error
    # with the message Not a JSON
    if not request.get_json():
        abort(400, "Not a JSON")
    # If the dictionary doesn't contain the key name, raise
    # a 400 error with the message Missing name
    if 'email' not in request.get_json().keys():
        abort(400, "Missing email")
    # If the dictionary doesn’t contain the key password, raise a
    # 400 error with the message Missing password
    if 'password' not in request.get_json().keys():
        abort(400, "Missing password")
    # Returns the new Amenity with the status code 201
    new_user = User(**request.get_json())
    new_user.save()
    return jsonify(new_user.to_dict()), 201


# Updates a user object: PUT /api/v1/users/<user_id>
@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def users_put(user_id):
    """Updates a user object"""
    user = storage.get(User, user_id)
    # If the user_id is not linked to any user object, raise a 404 error
    if not user:
        abort(404)
    # You must use request.get_json from Flask to transform the HTTP body
    # request to a dictionary
    # If the HTTP body request is not valid JSON, raise a 400 error
    # with the message Not a JSON
    if not request.get_json():
        abort(400, "Not a JSON")
    # Update the user object with all key-value pairs of the dictionary
    for key, value in request.get_json().items():
        # Ignore keys: id, email, created_at and updated_at
        if key in ["id", "email", "created_at", "updated_at"]:
            continue
        else:
            setattr(user, key, value)
    # Returns the user object with the status code 200
    storage.save()
    return jsonify(user.to_dict()), 200
