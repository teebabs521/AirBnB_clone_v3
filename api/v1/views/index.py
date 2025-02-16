#!/usr/bin/python3
"""Index file for API routes"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def status():
    """Returns API status"""
    return jsonify({"status": "OK"})

