from flask import jsonify, request
from models import storage
from models.state import State
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'])
def get_all_states():
    """ Retrieves the list of all State objects """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ Retrieves a State object """
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state)
    storage.save()
    return jsonify({})

@app_views.route('/states', methods=['POST'])
def create_state():
    """ Creates a new State object """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    state = State(name=data['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Updates a State object """
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    
    storage.save()
    return jsonify(state.to_dict())

