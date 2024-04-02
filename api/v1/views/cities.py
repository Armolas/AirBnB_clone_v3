#!/usr/bin/python3
"""This is the state view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def get_cities(city_id):
    """retrieves list of all state objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return city.to_dict()

    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        kwargs = request.get_json()
        for key in kwargs:
            if key not in ["id", "created_at", "updated_at"]:
                setattr(city, key, kwargs[key])
        city.save()
        return city.to_dict()

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def get_city(state_id):
    """retrieves a particular state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return cities

    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if "name" not in request.json:
            abort(400, "Missing name")
        kwargs = request.get_json()
        new_city = City(**kwargs)
        setattr(new_city, "state_id", state_id)
        storage.new(new_city)
        storage.save()
        return new_city.to_dict(), 201
