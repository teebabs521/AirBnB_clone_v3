
#!/usr/bin/python3
from flask import jsonify, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from uuid import UUID
from werkzeug.exceptions import NotFound, BadRequest

@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])

@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """ Retrieves an Amenity object by amenity_id """
    try:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            raise NotFound('Amenity not found')
        return jsonify(amenity.to_dict())
    except ValueError:
        raise NotFound('Amenity not found')

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        raise NotFound('Amenity not found')
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """ Creates a new Amenity """
    try:
        req_data = request.get_json()
        if req_data is None:
            raise BadRequest('Not a JSON')
        if 'name' not in req_data:
            raise BadRequest('Missing name')
        amenity = Amenity(name=req_data['name'])
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
    except BadRequest as e:
        raise BadRequest(str(e))

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ Updates an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        raise NotFound('Amenity not found')
    
    try:
        req_data = request.get_json()
        if req_data is None:
            raise BadRequest('Not a JSON')

        for key, value in req_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    except BadRequest as e:
        raise BadRequest(str(e))

