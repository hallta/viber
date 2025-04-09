"""
Cart model for the Viber application.
"""

from .. import db

class CartItem(db.Model):
    """CartItem model representing items in a user's shopping cart."""
    
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Relationships
    product = db.relationship('Product', back_populates='cart_items')
    
    def __repr__(self):
        """String representation of the cart item."""
        return f'<CartItem {self.product_id} ({self.quantity})>'
    
    def to_dict(self):
        """Convert cart item to dictionary."""
        return {
            'id': self.id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'total': self.product.price * self.quantity
        }
    
    @classmethod
    def get_cart_count(cls, session_id):
        """Get total number of items in cart for a session.
        
        Args:
            session_id: The session identifier
            
        Returns:
            int: Total number of items in cart
        """
        return cls.query.filter_by(session_id=session_id).count()
    
    @classmethod
    def clear_cart(cls, session_id):
        """Remove all items from cart for a session.
        
        Args:
            session_id: The session identifier
        """
        cls.query.filter_by(session_id=session_id).delete() 