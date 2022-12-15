#!/usr/bin/python3
"""Your first endpoint (route) will be to return the status of your API"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify
from flask_cors import CORS


# create a variable app, instance of Flask
app = Flask(__name__)
# register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)
# Update api/v1/app.py to create a CORS instance allowing: /* for 0.0.0.0
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


# declare a method to handle @app.teardown_appcontext
# that calls storage.close()
@app.teardown_appcontext
def teardown(self):
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    """inside if __name__ == "__main__":, run your Flask
    server (variable app) with"""
    if getenv('HBNB_MYSQL_HOST') and getenv('HBNB_API_PORT'):
        app.run(host=getenv('HBNB_MYSQL_HOST'), port=getenv('HBNB_API_PORT'),
                threaded=True)
    else:
        app.run(host='0.0.0.0', port='5000', threaded=True)

if __name__ == "__main__":
    app.url_map.strict_slashes = False
