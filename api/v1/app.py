#!/usr/bin/python3
"""This is the module for the app"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)
host = os.eniron.get('HBNB_API_HOST', '0.0.0.0')
port = int(os.environ.get('HBNB_API_PORT', 5000))


@app.teardown_appcontext
def close_storage(exception=None):
    """this methos handles the app teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handles a 404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
