"""
Order class (value object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from sqlalchemy import Column, Integer, Float, String, Boolean
from sqlalchemy.orm import relationship
from orders.models.base import Base

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    payment_link = Column(String, nullable=False)
    is_paid = Column(Boolean, nullable=False)
    
    # Relationship to order items
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
