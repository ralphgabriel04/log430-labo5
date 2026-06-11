"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import json
from db import get_redis_conn, get_sqlalchemy_session
from collections import defaultdict
from orders.models.order import Order
from orders.models.order_item import OrderItem
from sqlalchemy.sql import func

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    raw_order = r.hgetall(f"order:{order_id}")
    order = {}
    for key, value in raw_order.items():
        found_key = key.decode('utf-8') if isinstance(key, bytes) else key
        found_value = value.decode('utf-8') if isinstance(value, bytes) else value
        order[found_key] = found_value
    return order

def get_highest_spending_users_mysql():
    """Get report of highest spending users from MySQL"""
    session = get_sqlalchemy_session()
    limit = 10
    
    try:
        results = session.query(
            Order.user_id,
            func.sum(Order.total_amount).label('total_expense')
        ).group_by(Order.user_id)\
         .order_by(func.sum(Order.total_amount).desc())\
         .limit(limit)\
         .all()
        
        return [
            {
                "user_id": result.user_id,
                "total_expense": round(float(result.total_expense), 2)
            }
            for result in results
        ]
    finally:
        session.close()

def get_best_selling_products_mysql():
    """Get report of best selling products by quantity sold from MySQL"""
    session = get_sqlalchemy_session()
    limit = 100
    result = []
    
    try:
        order_items = session.query(
            OrderItem.product_id,
            func.sum(OrderItem.quantity).label('total_sold')
        ).group_by(OrderItem.product_id)\
         .order_by(func.sum(OrderItem.quantity).desc())\
         .limit(limit)\
         .all()
        
        for order_item in order_items:
            result.append({
                "product_id": order_item[0],
                "quantity": round(order_item[1], 2)
            })

        return result

    finally:
        session.close()

def get_highest_spending_users_redis():
    """Get report of highest spending users from Redis"""
    result = []
    try: 
        r = get_redis_conn()
        limit = 10
        order_keys = r.keys("order:*")
        spending = defaultdict(float)
        
        for key in order_keys:
            order_data = r.hgetall(key)
            if "user_id" in order_data and "total_amount" in order_data:
                user_id = int(order_data["user_id"])
                total = float(order_data["total_amount"])
                spending[user_id] += total

        # Trier par total dépensé (décroissant), limite X
        highest_spending_users = sorted(spending.items(), key=lambda x: x[1], reverse=True)[:limit]
        for user in highest_spending_users:
            result.append({
                "user_id": user[0],
                "total_expense": round(user[1], 2)
            })

    except Exception as e:
        return {'error': str(e)}

    return result

def get_best_selling_products_redis():
    """Get report of best selling products by quantity sold from Redis"""
    result = []

    try:
        r = get_redis_conn()
        limit = 10
        order_keys = r.keys("order:*")
        product_sales = defaultdict(int)
        
        for order_key in order_keys:
            order_data = r.hgetall(order_key)
            if "items" in order_data:
                try:
                    products = json.loads(order_data["items"])
                except Exception:
                    continue

                for item in products:
                    product_id = int(item.get("product_id", 0))
                    quantity = int(item.get("quantity", 0))
                    product_sales[product_id] += quantity

        # Trier par total vendu (décroissant), limite X
        best_selling = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:limit]
        for product in best_selling:
            result.append({
                "product_id": product[0],
                "quantity_sold": product[1]
            })

    except Exception as e:
        return {'error': str(e)}

    return result

def get_highest_spending_users():
    """ Get highest spending users report """
    return get_highest_spending_users_redis()

def get_best_selling_products():
    """ Get best selling products report """
    return get_best_selling_products_redis()