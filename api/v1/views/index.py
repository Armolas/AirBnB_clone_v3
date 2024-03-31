#!/usr/bin/python3
"""This is the index file"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """returns a status OK json"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def v1_stats():
    """retrieves the number of each objects by type"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models import storage
    count_dict = {}
    class_dict = {
            "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State,
            "users": User
            }
    for key, value in class_dict.items():
        count_dict[key] = storage.count(value)
    return jsonify(count_dict)
