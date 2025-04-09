"""
Cart routes for the Viber application.
"""

from typing import Any
from flask import Blueprint, request, session, jsonify
from ..models.cart import CartItem
from ..models.product import Product
from ..utils.decorators import login_required
from ..utils.template import render_template_with_nav
from .. import db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
@login_required
def view_cart() -> Any:
    """Display the shopping cart."""
    cart_items = CartItem.query.filter_by(session_id=session['username']).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template_with_nav('cart.html', 
                                  active_page='cart',
                                  cart_items=cart_items,
                                  total=total)

@cart_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id: int) -> Any:
    """Add a product to the cart."""
    product = Product.query.get_or_404(product_id)
    
    # Check if product already in cart
    cart_item = CartItem.query.filter_by(
        session_id=session['username'],
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            session_id=session['username'],
            product_id=product_id
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Product added to cart',
        'cart_count': CartItem.get_cart_count(session['username'])
    })

@cart_bp.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id: int) -> Any:
    """Update cart item quantity."""
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Ensure user owns this cart item
    if cart_item.session_id != session['username']:
        return jsonify({'error': 'Not authorized'}), 403
    
    data = request.get_json()
    quantity = data.get('quantity', 1)
    
    if quantity > 0:
        cart_item.quantity = quantity
        db.session.commit()
        return jsonify({'message': 'Cart updated'})
    else:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item removed from cart'})

@cart_bp.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id: int) -> Any:
    """Remove item from cart."""
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Ensure user owns this cart item
    if cart_item.session_id != session['username']:
        return jsonify({'error': 'Not authorized'}), 403
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({
        'message': 'Item removed from cart',
        'cart_count': CartItem.get_cart_count(session['username'])
    }) 