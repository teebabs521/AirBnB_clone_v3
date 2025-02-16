#!/usr/bin/python3
"""Index file for API routes"""
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'])
def status():
    """Returns API status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """Returns the number of each object type"""
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    stats = {key: storage.count(value) for key, value in classes.items()}
    return jsonify(stats)

