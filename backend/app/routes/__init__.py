"""
Routes Package
"""
from app.routes.auth import auth_bp
from app.routes.products import products_bp
from app.routes.categories import categories_bp
from app.routes.cart import cart_bp
from app.routes.orders import orders_bp
from app.routes.users import users_bp
from app.routes.chatbot import chatbot_bp

__all__ = [
    'auth_bp',
    'products_bp',
    'categories_bp',
    'cart_bp',
    'orders_bp',
    'users_bp',
    'chatbot_bp'
]
