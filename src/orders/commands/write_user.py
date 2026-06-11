"""
Users (write-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from orders.models.user import User
from db import get_sqlalchemy_session

def add_user(name: str, email: str):
    """Insert user with items in MySQL"""
    if not name or not email:
        raise ValueError("Cannot create user. A user must have name and email.")
    
    session = get_sqlalchemy_session()

    try: 
        new_user = User(name=name, email=email)
        session.add(new_user)
        session.flush() 
        session.commit()
        return new_user.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def delete_user(user_id: int):
    """Delete user in MySQL"""
    session = get_sqlalchemy_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return 1  
        else:
            return 0  
            
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

