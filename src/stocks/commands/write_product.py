"""
Products (write-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from stocks.models.product import Product
from db import get_sqlalchemy_session

def add_product(name: str, sku: str, price: float):
    """Insert product with items in MySQL"""
    if not name or not sku or not price or price <= 0:
        raise ValueError("Cannot create product. A product must have a name, SKU and price.")
    
    session = get_sqlalchemy_session()

    try: 
        new_product = Product(name=name, sku=sku, price=price)
        session.add(new_product)
        session.flush() 
        session.commit()
        return new_product.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def delete_product(product_id: int):
    """Delete product in MySQL"""
    session = get_sqlalchemy_session()
    try:
        product = session.query(Product).filter(Product.id == product_id).first()
        
        if product:
            session.delete(product)
            session.commit()
            return 1  
        else:
            return 0  
            
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

