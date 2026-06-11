"""
Product stock class (value object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from sqlalchemy import Column, Integer
from orders.models.base import Base

class Stock(Base):
    __tablename__ = 'stocks'
    product_id = Column(Integer, primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)