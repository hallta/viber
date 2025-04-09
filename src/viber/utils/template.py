"""
Template utilities for the Viber application.
"""

from typing import Any, Dict
from flask import render_template, session
from ..models.cart import CartItem

def render_template_with_nav(template_name: str, **context: Dict[str, Any]) -> str:
    """
    Render a template with common navigation context.
    
    Args:
        template_name: Name of the template to render
        **context: Template context variables
        
    Returns:
        str: Rendered template
    """
    # Add cart count to context if user is authenticated
    if session.get('authenticated'):
        cart_count = CartItem.get_cart_count(session['username'])
        context['cart_count'] = cart_count
    
    return render_template(template_name, **context) 