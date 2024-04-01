#!/usr/bin/python3
"""This is the state view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """retrieves list of all state objects"""
#    if request.method == 'GET':
    states = storage.all(State)
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return states_list

@app.route('/states', methods=['POST'])
def create_state():
#    if request.method == 'POST':
    if not request.json:
        abort(400, "Not a JSON")
    if not "name" in request.json:
        abort(400, "Missing name")
    new_state = State(**request.get_json())
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


#@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """retrieves a particular state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
#    if request.method == 'GET':
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_request(state_id):
#    if request.method == 'DELETE':
    for city in state.cities:
        city.delete()
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
#    if request.method == 'PUT':
    if not request.json:
        abort(400, "Not a JSON")
    kwargs = request.get_json()
    for key in kwargs:
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, kwargs[key])
    state.save()
    return jsonify(state.to_dict()), 200
