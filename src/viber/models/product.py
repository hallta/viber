"""
Product model for the Viber application.
"""

from .. import db

class Product(db.Model):
    """Product model representing items available for purchase."""
    
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    
    # Relationships
    cart_items = db.relationship('CartItem', back_populates='product', lazy='dynamic')
    
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
            'category': self.category
        } 