"""
Product controller
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from flask import jsonify
from stocks.commands.write_product import add_product, delete_product
from stocks.queries.read_product import get_product_by_id

def create_product(request):
    """Create product, use WriteProduct model"""
    payload = request.get_json() or {}
    name = payload.get('name')
    sku = payload.get('sku')
    price = payload.get('price')
    try:
        product_id = add_product(name, sku, price)
        return jsonify({'product_id': product_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def remove_product(product_id):
    """Delete product, use WriteProduct model"""
    try:
        deleted = delete_product(product_id)
        if deleted:
            return jsonify({'deleted': True})
        return jsonify({'deleted': False}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_product(product_id):
    """Create product, use ReadProduct model"""
    try:
        product = get_product_by_id(product_id)
        return jsonify(product), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500