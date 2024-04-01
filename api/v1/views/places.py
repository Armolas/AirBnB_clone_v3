#!/usr/bin/python3
"""The Place object view"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.places import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_city(city_id):
    """Get all Place objects of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_places_city(city_id):
    """Create a Place object in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    props = request.get_json()
    if "user_id" not in props:
        abort(400, "Missing user_id")
    if "name" not in request.json:
        abort(404, "Missing name")
    user = storage.get(User, props["user_id"])
    if user is None:
        abort(404)

    new_place = Place(**props)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Gets a Place object with specified place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object with the specified place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a place object with the specifed place_id"""
    place = storage.get(Place, place_id)
    if not request.json:
        abort(404, "Not a JSON")
    props = request.get_json()
    for key, value in props.items():
        if key not in ["id", "user_id", "city_id", "created_at",
                "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
