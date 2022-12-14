#!/usr/bin/python3
"""create a file index.py"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


# create a route /status on the object app_views
# that returns a JSON: "status": "OK"
@app_views.route("/status")
def status():
    return jsonify(status="OK")
# Create an endpoint that retrieves the number
# of each objects by type:


@app_views.route("/stats")
def status_count():
    data = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    }
    return data
