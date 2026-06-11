"""
SQLAlchemy Base Model
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from sqlalchemy.orm import declarative_base

# Create the shared declarative base that all models will inherit from
Base = declarative_base()