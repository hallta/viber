"""
Cart model for the Viber application.
"""

from ..extensions import db

class CartItem(db.Model):
    """CartItem model for storing items in user carts."""
    
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    session_id = db.Column(db.String(128), nullable=False)  # Store username as session ID
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    def __repr__(self):
        """String representation of the cart item."""
        return f'<CartItem {self.id}>'
    
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
        cart_items = cls.query.filter_by(session_id=session_id).all()
        return sum(item.quantity for item in cart_items)
    
    @classmethod
    def clear_cart(cls, session_id):
        """Remove all items from cart for a session.
        
        Args:
            session_id: The session identifier
        """
        cls.query.filter_by(session_id=session_id).delete()
        db.session.commit() 