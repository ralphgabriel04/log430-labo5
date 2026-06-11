"""
User controller
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from flask import jsonify
from orders.commands.write_user import add_user, delete_user
from orders.queries.read_user import get_user_by_id

def create_user(request):
    """Create user, use WriteUser model"""
    payload = request.get_json() or {}
    name = payload.get('name')
    email = payload.get('email')
    try:
        user_id = add_user(name, email)
        return jsonify({'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def remove_user(user_id):
    """Delete user, use WriteUser model"""
    try:
        deleted = delete_user(user_id)
        if deleted:
            return jsonify({'deleted': True})
        return jsonify({'deleted': False}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_user(user_id):
    """Create user, use ReadUser model"""
    try:
        user = get_user_by_id(user_id)
        return jsonify(user), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500