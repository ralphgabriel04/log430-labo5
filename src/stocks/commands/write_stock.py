"""
Product stocks (write-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from logger import Logger
from sqlalchemy import text
from stocks.models.product import Product
from stocks.models.stock import Stock
from db import get_redis_conn, get_sqlalchemy_session

# Si vous souhaitez en savoir plus sur le processus de logging, rendez-vous dans src/logger.py
logger = Logger.get_instance("store_manager")

def set_stock_for_product(product_id, quantity):
    """Set stock quantity for product in MySQL"""
    session = get_sqlalchemy_session()
    try: 
        result = session.execute(
            text(f"""
                UPDATE stocks 
                SET quantity = :qty 
                WHERE product_id = :pid
            """),
            {"pid": product_id, "qty": quantity}
        )
        response_message = f"rows updated: {result.rowcount}"
        if result.rowcount == 0:
            new_stock = Stock(product_id=product_id, quantity=quantity)
            session.add(new_stock)
            response_message = f"rows added, product id {new_stock.product_id}"
            session.flush() 
            session.commit()
  
        r = get_redis_conn()
        r.hset(f"stock:{product_id}", "quantity", quantity)
        return response_message
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
    
def update_stock_mysql(session, order_items, operation):
    """ Update stock quantities in MySQL according to a given operation (+/-) """
    try:
        for item in order_items:
            if hasattr(order_items[0], 'product_id'):
                pid = item.product_id
                qty = item.quantity
            else:
                pid = item['product_id']
                qty = item['quantity']
            session.execute(
                text(f"""
                    UPDATE stocks 
                    SET quantity = quantity {operation} :qty 
                    WHERE product_id = :pid
                """),
                {"pid": pid, "qty": qty}
            )
    except Exception as e:
        raise e
    
def check_out_items_from_stock(session, order_items):
    """ Decrease stock quantities in Redis """
    update_stock_mysql(session, order_items, "-")
    
def check_in_items_to_stock(session, order_items):
    """ Increase stock quantities in Redis """
    update_stock_mysql(session, order_items, "+")

def update_stock_redis(order_items, operation):
    """ Update stock quantities in Redis """
    if not order_items:
        return
    r = get_redis_conn()
    product_ids = []
    stock_keys = list(r.scan_iter("stock:*"))
    if stock_keys:
        pipeline = r.pipeline()
        for order_item in order_items:
            if hasattr(order_item, 'product_id'):
                product_ids.append(order_item.product_id)
            else:
                product_ids.append(order_item['product_id'])
            
        session = get_sqlalchemy_session()
        products_query = session.query(
                Product.id,
                Product.name,
                Product.sku,
                Product.price
            ).filter(Product.id.in_(product_ids))\
            .all()
        
        for order_item in order_items:
            if hasattr(order_item, 'product_id'):
                product_id = order_item.product_id
                quantity = order_item.quantity
            else:
                product_id = order_item['product_id']
                quantity = order_item['quantity']

            current_stock = r.hget(f"stock:{product_id}", "quantity")
            current_stock = int(current_stock) if current_stock else 0
            
            if operation == '+':
                new_quantity = current_stock + quantity
            else:  
                new_quantity = current_stock - quantity

            order_item_product = {}
            for product in products_query:
                if product[0] == product_id:
                    order_item_product['name'] = product[1] 
                    order_item_product['sku'] = product[2] 
                    order_item_product['unit_price'] = product[3] 

            pipeline.hset(f"stock:{product_id}", mapping={ 
                "product_name": order_item_product['name'], 
                "product_sku": order_item_product['sku'], 
                "product_unit_price": order_item_product['unit_price'], 
                "quantity": new_quantity 
            })
        
        pipeline.execute()
    
    else:
        populate_redis_from_mysql(r)

def populate_redis_from_mysql(redis_conn):
    """ Helper function to populate Redis from MySQL stocks table """
    session = get_sqlalchemy_session()
    try:
        stocks_in_mysql = session.execute(
            text("SELECT product_id, quantity FROM stocks")
        ).fetchall()
        stocks_in_redis = redis_conn.keys(f"stock:*")
        if not len(stocks_in_mysql) or len(stocks_in_redis) > 0:
            logger.debug("Il n'est pas nécessaire de synchronisér le stock MySQL avec Redis")
            return
        
        pipeline = redis_conn.pipeline()
        
        for product_id, quantity in stocks_in_mysql:
            pipeline.hset(
                f"stock:{product_id}", 
                mapping={ "quantity": quantity }
            )
        
        pipeline.execute()
        logger.debug(f"{len(stocks_in_mysql)} enregistrements de stock ont été synchronisés avec Redis")
        
    except Exception as e:
        logger.debug(f"Erreur de synchronisation: {e}")
        raise e
    finally:
        session.close()