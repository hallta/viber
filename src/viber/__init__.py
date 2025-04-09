"""
Viber web application package.
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask extensions
db = SQLAlchemy()

def create_app(config=None):
    """Create and configure the Flask application.
    
    Args:
        config: Configuration object or dictionary
        
    Returns:
        Flask: Configured Flask application
    """
    # Create Flask app with template folder in root directory
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'static'))
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    # Default configuration
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///viber.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Override with provided config
    if config:
        app.config.update(config)
    
    # Initialize extensions with app
    db.init_app(app)
    
    # Register blueprints
    from .routes import auth_bp, cart_bp, pages_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(pages_bp)
    
    return app 