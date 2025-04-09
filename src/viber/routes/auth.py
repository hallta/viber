"""
Authentication routes for the Viber application.
"""

from typing import Any
from flask import Blueprint, request, session, redirect, url_for, flash
from ..utils.template import render_template_with_nav

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> Any:
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # For now, accept any username/password
        if username and password:
            session['authenticated'] = True
            session['username'] = username
            flash('Successfully logged in!', 'success')
            
            # Get next URL from form or query string
            next_url = request.form.get('next') or request.args.get('next')
            if next_url:
                # Make sure we only redirect to relative URLs
                if not next_url.startswith('/'):
                    next_url = '/'
                return redirect(next_url)
            return redirect(url_for('pages.home'))
        
        flash('Please provide both username and password', 'error')
    
    # Get the next parameter from the query string for the form
    next_url = request.args.get('next', '')
    return render_template_with_nav('login.html', active_page='login', next=next_url)

@auth_bp.route('/logout')
def logout() -> Any:
    """Handle user logout without clearing cart."""
    session.pop('authenticated', None)
    session.pop('username', None)
    flash('Successfully logged out!', 'success')
    return redirect(url_for('pages.home'))

@auth_bp.route('/logout/clear-cart')
def logout_and_clear_cart() -> Any:
    """Handle user logout and clear their cart."""
    from ..models.cart import CartItem
    
    if 'username' in session:
        CartItem.clear_cart(session['username'])
    
    session.pop('authenticated', None)
    session.pop('username', None)
    flash('Successfully logged out and cleared cart!', 'success')
    return redirect(url_for('pages.home')) 