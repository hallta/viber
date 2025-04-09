"""
Database initialization script for Viber.
"""

from viber import create_app, db
from viber.models.product import Product

def init_db():
    """Initialize the database with tables and sample data."""
    app = create_app()
    with app.app_context():
        # Create all tables
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
            print("Database initialized with sample products.")
        else:
            print("Database already contains products.")

if __name__ == '__main__':
    init_db() 