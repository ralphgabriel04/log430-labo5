"""
Tests for orders manager
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import json
import uuid
from logger import Logger
import pytest
from store_manager import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    result = client.get('/health-check')
    assert result.status_code == 200
    assert result.get_json() == {'status':'ok'}

def test_stock_flow(client):
    """Smoke test for complete stock management flow"""
    logger = Logger.get_instance("test")
    
    # 1. Create a product (POST /products)
    product_data = {
        'name': 'Test Product', 
        'sku': 'TEST-SKU-001', 
        'price': 49.99
    }
    response = client.post('/products',
                          data=json.dumps(product_data),
                          content_type='application/json')
    
    assert response.status_code == 201, f"Failed to create product: {response.get_json()}"
    product_id = response.get_json()['product_id']
    assert product_id > 0
    logger.debug(f"Created product with ID: {product_id}")
    
    # 2. Add 5 units to stock (POST /stocks)
    stock_data = {
        'product_id': product_id,
        'quantity': 5
    }
    response = client.post('/stocks',
                          data=json.dumps(stock_data),
                          content_type='application/json')
    
    assert response.status_code == 201, f"Failed to set stock: {response.get_json()}"
    logger.debug(f"Set stock to 5 units for product {product_id}")
    
    # 3. Verify stock - should have 5 units (GET /stocks/:id)
    response = client.get(f'/stocks/{product_id}')
    assert response.status_code == 201, f"Failed to get stock: {response.get_json()}"
    stock_data = response.get_json()
    assert stock_data['product_id'] == product_id
    assert stock_data['quantity'] == 5
    logger.debug(f"Stock verified: {stock_data['quantity']} units")
    
    # Create a user for the order. User emails MUST be unique.
    random_email_address = f"t{uuid.uuid1()}@example.com"
    user_data = {'name': 'Test User', 'email': random_email_address}
    response = client.post('/users',
                          data=json.dumps(user_data),
                          content_type='application/json')
    assert response.status_code == 201, f"Failed to create user: {response.get_json()}"
    user_id = response.get_json()['user_id']
    logger.debug(f"Created user with ID: {user_id}")
    
    # 4. Create an order with 2 units (POST /orders)
    order_data = {
        'user_id': user_id,
        'items': [
            {
                'product_id': product_id,
                'quantity': 2
            }
        ]
    }
    response = client.post('/orders',
                          data=json.dumps(order_data),
                          content_type='application/json')
    
    assert response.status_code == 201, f"Failed to create order: {response.get_json()}"
    order_id = response.get_json()['order_id']
    assert order_id > 0
    logger.debug(f"Created order with ID: {order_id}")
    
    # 5. Verify stock again - should have 3 units (5 - 2) (GET /stocks/:id)
    response = client.get(f'/stocks/{product_id}')
    assert response.status_code == 201, f"Failed to get stock after order: {response.get_json()}"
    stock_data = response.get_json()
    assert stock_data['product_id'] == product_id
    assert stock_data['quantity'] == 3, f"Expected 3 units, got {stock_data['quantity']}"
    logger.debug(f"Stock after order: {stock_data['quantity']} units")