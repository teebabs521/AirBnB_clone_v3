#!/usr/bin/python3
"""Places view for the API"""

from flask import jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


# Retrieves the list of all Place objects of a City: GET /api/v1/cities/<city_id>/places
@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404

    places = storage.all(Place).values()
    city_places = [place.to_dict() for place in places if place.city_id == city_id]
    return jsonify(city_places)


# Retrieves a Place object: GET /api/v1/places/<place_id>
@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())


# Deletes a Place object: DELETE /api/v1/places/<place_id>
@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


# Creates a Place: POST /api/v1/cities/<city_id>/places
@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404

    try:
        req_data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    if 'user_id' not in req_data:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, req_data['user_id'])
    if not user:
        return jsonify({"error": "User not found"}), 404

    if 'name' not in req_data:
        return jsonify({"error": "Missing name"}), 400

    new_place = Place(
        name=req_data['name'],
        user_id=req_data['user_id'],
        city_id=city_id
    )
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


# Updates a Place object: PUT /api/v1/places/<place_id>
@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404

    try:
        req_data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in req_data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict())

