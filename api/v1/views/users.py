from flask import jsonify, request
from models import storage
from models.user import User
from api.v1.views import app_views
from werkzeug.exceptions import NotFound, BadRequest

@app_views.route('/users', methods=['GET'])
def get_users():
    """ Retrieves the list of all User objects """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])

@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ Retrieves a User object by user_id """
    try:
        user = storage.get(User, user_id)
        if user is None:
            raise NotFound('User not found')
        return jsonify(user.to_dict())
    except ValueError:
        raise NotFound('User not found')

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if user is None:
        raise NotFound('User not found')
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'])
def create_user():
    """ Creates a new User """
    try:
        req_data = request.get_json()
        if req_data is None:
            raise BadRequest('Not a JSON')
        if 'email' not in req_data:
            raise BadRequest('Missing email')
        if 'password' not in req_data:
            raise BadRequest('Missing password')
        user = User(email=req_data['email'], password=req_data['password'])
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201
    except BadRequest as e:
        raise BadRequest(str(e))

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ Updates a User object """
    user = storage.get(User, user_id)
    if user is None:
        raise NotFound('User not found')
    
    try:
        req_data = request.get_json()
        if req_data is None:
            raise BadRequest('Not a JSON')

        for key, value in req_data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    except BadRequest as e:
        raise BadRequest(str(e))

