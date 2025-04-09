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
    flash
)
from functools import wraps
from typing import Dict, Any, Callable

# Initialize Flask application
app = Flask(__name__)
# Set a secret key for session management (in production, use a secure secret key)
app.secret_key = 'dev-secret-key'  # Change this in production!

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
    return render_template(template_name, active_page=active_page, **kwargs)

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
    session.clear()
    flash('Successfully logged out!', 'success')
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

if __name__ == '__main__':
    # Run the application on all network interfaces
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False  # Set to True for development
    ) 