"""
Page routes for the Viber application.
"""

from typing import Any
from flask import Blueprint, render_template, session, request
from sqlalchemy import or_, and_
from ..models.product import Product, CATEGORIES, FITS, SIZES, COLORS, MATERIALS, STYLES, SEASONS, GENDERS
from ..extensions import db
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
    # Get filter parameters from request
    selected_filters = {
        'category': request.args.getlist('category'),
        'style': request.args.getlist('style'),
        'size': request.args.getlist('size'),
        'color': request.args.getlist('color'),
        'gender': request.args.getlist('gender'),
        'season': request.args.getlist('season'),
        'min_price': request.args.get('min_price', type=float),
        'max_price': request.args.get('max_price', type=float),
        'in_stock': request.args.get('in_stock') == 'true'
    }

    # Build the query
    query = Product.query

    # Apply filters
    if selected_filters['category']:
        query = query.filter(Product.category.in_(selected_filters['category']))
    if selected_filters['style']:
        query = query.filter(Product.style.in_(selected_filters['style']))
    if selected_filters['size']:
        query = query.filter(Product.size.in_(selected_filters['size']))
    if selected_filters['color']:
        query = query.filter(Product.color.in_(selected_filters['color']))
    if selected_filters['gender']:
        query = query.filter(Product.gender.in_(selected_filters['gender']))
    if selected_filters['season']:
        query = query.filter(Product.season.in_(selected_filters['season']))
    if selected_filters['min_price'] is not None:
        query = query.filter(Product.price >= selected_filters['min_price'])
    if selected_filters['max_price'] is not None:
        query = query.filter(Product.price <= selected_filters['max_price'])
    if selected_filters['in_stock']:
        query = query.filter(Product.in_stock == True)

    # Apply sorting
    sort = request.args.get('sort', 'featured')
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'name_asc':
        query = query.order_by(Product.name.asc())
    elif sort == 'name_desc':
        query = query.order_by(Product.name.desc())

    # Execute query
    products = query.all()

    # Get cart count for authenticated users
    cart_count = 0
    if session.get('authenticated'):
        cart = session.get('cart', {})
        cart_count = sum(cart.values())

    return render_template_with_nav('products.html',
                         active_page='products',
                         products=products,
                         cart_count=cart_count,
                         categories=CATEGORIES,
                         styles=STYLES,
                         sizes=SIZES,
                         colors=COLORS,
                         genders=GENDERS,
                         seasons=SEASONS,
                         selected_filters=selected_filters,
                         sort_by=sort) 