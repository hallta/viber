"""
Route blueprints for the Viber application.
"""

from .auth import auth_bp
from .cart import cart_bp
from .pages import pages_bp

__all__ = ['auth_bp', 'cart_bp', 'pages_bp'] 