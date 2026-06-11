"""
Product (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from db import get_sqlalchemy_session
from stocks.models.product import Product
from stocks.models.stock import Stock

def get_stock_by_id(product_id):
    """Get stock by product ID """
    session = get_sqlalchemy_session()
    result = session.query(Stock).filter_by(product_id=product_id).all()
    if len(result):
        return {
            'product_id': result[0].product_id,
            'quantity': result[0].quantity,
        }
    else:
        return {}

def get_stock_for_all_products():
    """Get stock quantity for all products"""
    session = get_sqlalchemy_session()
    results = session.query(
        Stock.product_id,
        Stock.quantity,
        Product.name,
        Product.sku,
        Product.price
    ).join(Product, Product.id == Stock.product_id).all()
    stock_data = []
    for row in results:
        stock_data.append({
            'Article': row.name,
            'Numéro SKU': row.sku,
            'Prix unitaire': float(row.price),
            'Unités en stock': int(row.quantity),
        })
    
    return stock_data
