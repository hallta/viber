#!/usr/bin/env python3
"""
Viber Web Application
A simple Flask web server that serves a website with navigation.

This module contains the main Flask application and route definitions.
"""

from flask import Flask, render_template
from typing import Dict, Any

# Initialize Flask application
app = Flask(__name__)

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

@app.route('/')
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