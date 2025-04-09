#!/usr/bin/env python3
"""
Viber Web Application
A simple Flask web server that serves a website with navigation and authentication.

This module contains the main Flask application and route definitions.
"""

from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    session, 
    flash,
    jsonify
)
from functools import wraps
from typing import Dict, Any, Callable
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)
# Set a secret key for session management (in production, use a secure secret key)
app.secret_key = 'dev-secret-key'  # Change this in production!

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hats.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship to get product details
    product = db.relationship('Product', backref='cart_items')

# Create tables
with app.app_context():
    db.create_all()
    # Add sample data if the products table is empty
    if not Product.query.first():
        sample_products = [
            Product(
                name='Classic Fedora',
                description='A timeless fedora hat made from premium felt',
                price=49.99,
                image_url='https://placehold.co/300x200?text=Fedora',
                category='Formal'
            ),
            Product(
                name='Summer Straw Hat',
                description='Light and breezy straw hat perfect for sunny days',
                price=29.99,
                image_url='https://placehold.co/300x200?text=Straw+Hat',
                category='Summer'
            ),
            Product(
                name='Winter Beanie',
                description='Warm and cozy beanie for cold weather',
                price=19.99,
                image_url='https://placehold.co/300x200?text=Beanie',
                category='Winter'
            ),
            Product(
                name='Vintage Bowler',
                description='Classic bowler hat with a modern twist',
                price=59.99,
                image_url='https://placehold.co/300x200?text=Bowler',
                category='Formal'
            )
        ]
        db.session.bulk_save_objects(sample_products)
        db.session.commit()

def login_required(f: Callable) -> Callable:
    """
    Decorator to require login for routes.
    
    Args:
        f: The route function to wrap
    
    Returns:
        Callable: The wrapped function
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if 'authenticated' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def render_template_with_nav(template_name: str, active_page: str, **kwargs: Dict[str, Any]) -> str:
    """
    Helper function to render templates with navigation context.
    
    Args:
        template_name: Name of the template file to render
        active_page: Current active page for navigation highlighting
        **kwargs: Additional template variables
    
    Returns:
        str: Rendered HTML template
    """
    cart_count = get_cart_count()
    return render_template(template_name, active_page=active_page, cart_count=cart_count, **kwargs)

@app.route('/login', methods=['GET', 'POST'])
def login() -> Any:
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # For now, accept any username/password
        if username and password:
            session['authenticated'] = True
            session['username'] = username
            next_page = request.args.get('next')
            flash('Successfully logged in!', 'success')
            return redirect(next_page or url_for('home'))
        
        flash('Please provide both username and password', 'error')
    
    return render_template_with_nav('login.html', active_page='login')

@app.route('/logout')
def logout() -> Any:
    """Handle user logout."""
    # Only clear the session, keep cart items
    session.clear()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('login'))

@app.route('/logout/clear-cart')
def logout_and_clear_cart() -> Any:
    """Handle user logout and clear their cart."""
    username = session.get('username')
    if session.get('authenticated') and username:
        # Clear cart items for the current user
        CartItem.query.filter_by(session_id=username).delete()
        db.session.commit()
    
    session.clear()
    flash('Successfully logged out and cleared cart!', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home() -> str:
    """Render the home page."""
    return render_template_with_nav('index.html', active_page='home')

@app.route('/about')
def about() -> str:
    """Render the about page."""
    return render_template_with_nav('about.html', active_page='about')

@app.route('/contact')
def contact() -> str:
    """Render the contact page."""
    return render_template_with_nav('contact.html', active_page='contact')

def get_cart_count():
    """Helper function to get the number of items in cart"""
    if not session.get('authenticated'):
        return 0
    return CartItem.query.filter_by(session_id=session.get('username')).count()

@app.before_request
def before_request():
    """Ensure cart session is tied to authenticated user"""
    if session.get('authenticated') and not session.get('session_id'):
        session['session_id'] = session.get('username')

@app.route('/products')
def products():
    """Render the products page"""
    products = Product.query.all()
    cart_count = get_cart_count()
    return render_template('products.html', products=products, active_page='products', cart_count=cart_count)

@app.route('/cart')
@login_required
def view_cart():
    """Render the cart page"""
    cart_items = CartItem.query.filter_by(session_id=session.get('username')).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    cart_count = get_cart_count()
    return render_template('cart.html', 
                         cart_items=cart_items, 
                         total=total, 
                         active_page='cart',
                         cart_count=cart_count)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Add a product to cart"""
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem.query.filter_by(
        session_id=session.get('username'),
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            session_id=session.get('username'),
            product_id=product_id
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'Added {product.name} to cart!', 'success')
    return jsonify({
        'message': 'Added to cart',
        'cart_count': get_cart_count()
    })

@app.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    """Update cart item quantity"""
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.session_id != session.get('username'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    quantity = request.json.get('quantity', 0)
    if quantity > 0:
        cart_item.quantity = quantity
        db.session.commit()
        return jsonify({'message': 'Updated'})
    else:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Removed'})

@app.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    """Remove item from cart"""
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.session_id != session.get('username'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart!', 'success')
    return jsonify({'message': 'Removed'})

if __name__ == '__main__':
    # Run the application on all network interfaces
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False  # Set to True for development
    ) 