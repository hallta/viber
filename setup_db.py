"""
Database setup script for Viber.
"""

import os
from src.viber import create_app, db
from src.viber.models.product import Product

def setup_db():
    """Set up the database with tables and initial data."""
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    # Remove existing database if it exists
    if os.path.exists('instance/viber.db'):
        os.remove('instance/viber.db')
    
    app = create_app()
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Add test product
        test_product = Product(
            name='Test Hat',
            description='A test hat',
            price=29.99,
            image_url='https://test.com/hat.jpg',
            category='T-Shirts',
            fit='Regular',
            size='M',
            color='Black',
            material='Cotton',
            style='Casual',
            season='All-Season',
            gender='Unisex',
            in_stock=True,
            stock_quantity=10
        )
        db.session.add(test_product)
        db.session.commit()
        
        # Verify the database was created correctly
        product = Product.query.first()
        if product and all(hasattr(product, attr) for attr in [
            'fit', 'size', 'color', 'material', 'style', 'season', 'gender'
        ]):
            print("Database initialized successfully with all required columns.")
        else:
            print("Error: Database initialization failed - missing columns.")
            return False
    
    return True

if __name__ == '__main__':
    if not setup_db():
        exit(1) 