#!/usr/bin/python3
"""Cities API routes"""
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieve all City objects of a given State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve a City object by ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a City object by ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a new City in a given State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")

    new_city = City(name=data["name"], state_id=state_id)
    storage.new(new_city)
    storage.save()
    
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update an existing City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    # Ignore keys: id, state_id, created_at, updated_at
    ignored_keys = {"id", "state_id", "created_at", "updated_at"}
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200

