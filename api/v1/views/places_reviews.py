#!/usr/bin/python3
"""Create a new view for Review object that handles
all default RESTFul API actions:"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


# Retrieves the list of all Review objects of a Place: GET
# /api/v1/places/<place_id>/reviews
@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def get_reviews_by_places(place_id):
    place = storage.get(Place, place_id)
    # If the place_id is not linked to any Place object,
    # raise a 404 error
    if not place:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


# Retrieves a Review object. : GET
# /api/v1/reviews/<review_id>
@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def reviews_by_id(review_id):
    """retrieves the reviews"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    # If the review_id is not linked to any Review object, raise a 404 error
    abort(404)


# Deletes a Review object: DELETE /api/v1/reviews/<review_id>
@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """deletes a Amenity"""
    review = storage.get(Review, review_id)
    if not review:
        # If the review_id is not linked to any Review object,
        # raise a 404 error
        abort(404)
    review.delete()
    storage.save()
    # Returns an empty dictionary with the status code 200
    return jsonify({}), 200


# Creates a Review: POST /api/v1/places/<place_id>/reviews
@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def review_post(place_id):
    """You must use request.get_json from Flask to
    transform the HTTP body request to a dictionary"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    # If the HTTP body request is not valid JSON, raise a 400 error
    # with the message Not a JSON
    if not request.get_json():
        abort(400, "Not a JSON")
    # If the dictionary doesn't contain the key name, raise
    # a 400 error with the message Missing name
    if 'user_id' not in request.get_json().keys():
        abort(400, "Missing user_id")
    # If the dictionary doesn’t contain the key text, raise a
    # 400 error with the message Missing text
    if 'text' not in request.get_json().keys():
        abort(400, "Missing text")
    # If the user_id is not linked to any User object, raise a 404 error
    valid_user = storage.get(User, request.get_json()['user_id'])
    if not valid_user:
        abort(404)
    # Returns the new Amenity with the status code 201
    new_review = Review(**request.get_json())
    setattr(new_review, 'place_id', place_id)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


# Updates a Review object: PUT /api/v1/reviews/<review_id>
@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def review_put(review_id):
    """Updates a review object"""
    review = storage.get(Review, review_id)
    # If the review_id is not linked to any Review object, raise a 404 error
    if not review:
        abort(404)
    # You must use request.get_json from Flask to transform the HTTP body
    # request to a dictionary
    # If the HTTP body request is not valid JSON, raise a 400 error
    # with the message Not a JSON
    if not request.get_json():
        abort(400, "Not a JSON")
    # Update the place object with all key-value pairs of the dictionary
    for key, value in request.get_json().items():
        # Ignore keys: id, user_id, place_id, created_at and updated_at
        if key in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            continue
        else:
            setattr(review, key, value)
    # Returns the place object with the status code 200
    storage.save()
    return jsonify(review.to_dict()), 200
