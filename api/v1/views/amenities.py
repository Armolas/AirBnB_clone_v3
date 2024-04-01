#!/usr/bin/python3
"""The Amenities View"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenties():
    """Gets all amenities"""
    all_amenities = storage.all(Amenity)
    amenities = [amenity.to_dict() for amenity in all_amenities.values()]
    return amenities

@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates an amenity object"""
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    props = request.get_json()
    new_amenity = Amenity(**props)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_state(amenity_id):
    """Gets the amenity object of a specified amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('./amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete an amenity object with the specified amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an amentiy object for a specified amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        abort(404)
    props = request.get_json()
    for key, value in props.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
