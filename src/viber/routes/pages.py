"""
Page routes for the Viber application.
"""

from typing import Any
from flask import Blueprint
from ..models.product import Product
from ..utils.template import render_template_with_nav

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def home() -> Any:
    """Display the home page."""
    return render_template_with_nav('home.html', active_page='home')

@pages_bp.route('/about')
def about() -> Any:
    """Display the about page."""
    return render_template_with_nav('about.html', active_page='about')

@pages_bp.route('/contact')
def contact() -> Any:
    """Display the contact page."""
    return render_template_with_nav('contact.html', active_page='contact')

@pages_bp.route('/products')
def products() -> Any:
    """Display the products page."""
    products = Product.query.all()
    return render_template_with_nav('products.html',
                                  active_page='products',
                                  products=products) 