#!/usr/bin/python3
"""Reviews view for the API"""

from flask import jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


# Retrieves the list of all Review objects of a Place: GET /api/v1/places/<place_id>/reviews
@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404

    reviews = storage.all(Review).values()
    place_reviews = [review.to_dict() for review in reviews if review.place_id == place_id]
    return jsonify(place_reviews)


# Retrieves a Review object: GET /api/v1/reviews/<review_id>
@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({"error": "Not found"}), 404
    return jsonify(review.to_dict())


# Deletes a Review object: DELETE /api/v1/reviews/<review_id>
@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({"error": "Not found"}), 404

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


# Creates a Review: POST /api/v1/places/<place_id>/reviews
@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
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

    if 'text' not in req_data:
        return jsonify({"error": "Missing text"}), 400

    new_review = Review(
        text=req_data['text'],
        user_id=req_data['user_id'],
        place_id=place_id
    )
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


# Updates a Review object: PUT /api/v1/reviews/<review_id>
@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({"error": "Not found"}), 404

    try:
        req_data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in req_data.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict())

