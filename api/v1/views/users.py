#!/usr/bin/python3
"""The User object view"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
def get_users():
    """Get the list of all User objects"""
    all_users = storage.all(User)
    users = [user.to_dict() for user in all_users.values()]
    if request.method == 'GET':
        return jsonify(users)

    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        props = request.get_json()
        if "email" not in props:
            abort(400, "Missing email")
        if "password" not in props:
            abort(400, "Missing password")
        new_user = User(**props)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_user(user_id):
    """Get a User object with the specified user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        props = request.get_json()
        for key, value in props.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200