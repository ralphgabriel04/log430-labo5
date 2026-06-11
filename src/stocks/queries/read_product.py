"""
Product (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from db import get_sqlalchemy_session
from stocks.models.product import Product

def get_product_by_id(product_id):
    """Get product by ID """
    session = get_sqlalchemy_session()
    result = session.query(Product).filter_by(id=product_id).all()

    if len(result):
        return {
            'id': result[0].id,
            'name': result[0].name,
            'sku': result[0].sku,
            'price': result[0].price
        }
    else:
        return {}


