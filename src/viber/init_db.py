"""
Database initialization script for Viber.
"""

import os
import random
from viber import create_app, db
from viber.models.product import Product

# Product attributes for generating diverse items
CATEGORIES = ['T-Shirts', 'Shirts', 'Pants', 'Jeans', 'Dresses', 'Skirts', 'Jackets', 'Coats', 'Sweaters', 'Hoodies']
FITS = ['Regular', 'Slim', 'Relaxed', 'Oversized', 'Fitted', 'Loose']
SIZES = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
COLORS = ['Black', 'White', 'Navy', 'Gray', 'Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Pink', 'Brown', 'Beige']
MATERIALS = ['Cotton', 'Polyester', 'Wool', 'Linen', 'Denim', 'Silk', 'Leather', 'Canvas', 'Fleece']
STYLES = ['Casual', 'Formal', 'Sport', 'Vintage', 'Modern', 'Classic', 'Streetwear', 'Business']
SEASONS = ['Spring', 'Summer', 'Fall', 'Winter', 'All-Season']
GENDERS = ['Men', 'Women', 'Unisex']

def generate_price():
    """Generate a random price between 19.99 and 199.99."""
    return round(random.uniform(19.99, 199.99), 2)

def generate_description(name, material, style, fit):
    """Generate a product description."""
    return f"A {style.lower()} {name.lower()} made from premium {material.lower()}. " \
           f"Features a {fit.lower()} fit that's perfect for any occasion."

def generate_products(count=100):
    """Generate a list of diverse products."""
    products = []
    for _ in range(count):
        category = random.choice(CATEGORIES)
        style = random.choice(STYLES)
        material = random.choice(MATERIALS)
        fit = random.choice(FITS)
        name = f"{style} {material} {category.rstrip('s')}"
        in_stock = random.choice([True, True, True, False])  # 75% chance of being in stock
        
        products.append(Product(
            name=name,
            description=generate_description(name, material, style, fit),
            price=generate_price(),
            image_url=f'https://placehold.co/300x200?text={name.replace(" ", "+")}',
            category=category,
            fit=fit,
            size=random.choice(SIZES),
            color=random.choice(COLORS),
            material=material,
            style=style,
            season=random.choice(SEASONS),
            gender=random.choice(GENDERS),
            in_stock=in_stock,
            stock_quantity=random.randint(0, 50) if in_stock else 0
        ))
    return products

def init_db():
    """Initialize the database with tables and sample data."""
    app = create_app()
    
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Add sample data
        products = generate_products(100)
        db.session.bulk_save_objects(products)
        db.session.commit()
        print("Database initialized with 100 sample products.")

if __name__ == '__main__':
    init_db() 