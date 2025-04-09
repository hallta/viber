"""
Viber web application package.
"""

import os
from flask import Flask
from .extensions import db, migrate
from .routes.auth import auth_bp

# Import models to ensure they are registered with SQLAlchemy
from .models.product import Product
from .models.cart import CartItem

def create_app(config=None):
    """Create and configure the Flask application.
    
    Args:
        config: Configuration object or dictionary to override defaults
        
    Returns:
        Configured Flask application instance
    """
    # Create Flask app with template folder in root directory
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'static'))
    instance_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'instance'))
    
    # Ensure instance directory exists
    os.makedirs(instance_dir, exist_ok=True)
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir,
                instance_path=instance_dir)
    
    # Default configuration
    db_path = os.path.join(instance_dir, 'viber.db')
    app.config.update(
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY='dev'  # Set a default secret key
    )
    
    # Override defaults with passed config
    if config:
        app.config.update(config)
    
    # Ensure SECRET_KEY is set
    if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = 'dev'
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from .routes import auth_bp, cart_bp, pages_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(pages_bp)
    
    return app 