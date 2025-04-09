"""
Product model for the Viber application.
"""

from ..extensions import db

# Constants for product attributes
CATEGORIES = ['T-Shirts', 'Shirts', 'Pants', 'Jeans', 'Dresses', 'Skirts', 'Jackets', 'Coats', 'Sweaters', 'Hoodies']
FITS = ['Regular', 'Slim', 'Relaxed', 'Oversized', 'Fitted', 'Loose']
SIZES = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
COLORS = ['Black', 'White', 'Navy', 'Gray', 'Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Pink', 'Brown', 'Beige']
MATERIALS = ['Cotton', 'Polyester', 'Wool', 'Linen', 'Denim', 'Silk', 'Leather', 'Canvas', 'Fleece']
STYLES = ['Casual', 'Formal', 'Sport', 'Vintage', 'Modern', 'Classic', 'Streetwear', 'Business']
SEASONS = ['Spring', 'Summer', 'Fall', 'Winter', 'All-Season']
GENDERS = ['Men', 'Women', 'Unisex']

class Product(db.Model):
    """Product model for storing product items."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False, default=CATEGORIES[0])
    fit = db.Column(db.String(50), nullable=False, default=FITS[0])
    size = db.Column(db.String(10), nullable=False, default=SIZES[2])  # Default to M
    color = db.Column(db.String(20), nullable=False, default=COLORS[0])
    material = db.Column(db.String(50), nullable=False, default=MATERIALS[0])
    style = db.Column(db.String(50), nullable=False, default=STYLES[0])
    season = db.Column(db.String(20), nullable=False, default=SEASONS[-1])  # Default to All-Season
    gender = db.Column(db.String(10), nullable=False, default=GENDERS[-1])  # Default to Unisex
    in_stock = db.Column(db.Boolean, default=True)
    stock_quantity = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Define relationships
    cart_items = db.relationship('CartItem', backref='product', lazy=True)

    def __repr__(self):
        """String representation of the product."""
        return f'<Product {self.name}>'

    def to_dict(self):
        """Convert product to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'category': self.category,
            'fit': self.fit,
            'size': self.size,
            'color': self.color,
            'material': self.material,
            'style': self.style,
            'season': self.season,
            'gender': self.gender,
            'in_stock': self.in_stock,
            'stock_quantity': self.stock_quantity
        } 