"""
User model for the Viber application.
"""
from ..extensions import db

class User(db.Model):
    """User model for storing user accounts."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        """String representation of the user."""
        return f'<User {self.username}>' 