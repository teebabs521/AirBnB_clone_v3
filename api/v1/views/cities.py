#!/usr/bin/python3

from flask import Flask, request, jsonify
from models import storage
from models.city import City
from models.state import State
from uuid import UUID

# Retrieve all cities of a state
@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_of_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities  # Assuming State has a relationship with City
    return jsonify([city.to_dict() for city in cities])

# Retrieve a single city by ID
@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

# Delete a city by ID
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})

# Create a new city
@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")
    city = City(name=data['name'], state_id=state_id)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201

# Update a city by ID
@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())

