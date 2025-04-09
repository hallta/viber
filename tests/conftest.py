"""
Test configuration and fixtures for the Viber application.
"""

import pytest
from viber import create_app, db
from viber.models.product import Product

@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })
    
    with app.app_context():
        db.create_all()
        
        # Add test product
        test_product = Product(
            name='Test Hat',
            description='A test hat',
            price=29.99,
            image_url='https://test.com/hat.jpg',
            category='Test'
        )
        db.session.add(test_product)
        db.session.commit()
    
    yield app
    
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()

@pytest.fixture
def auth(client):
    """Authentication helper class."""
    class AuthActions:
        def __init__(self, client):
            self._client = client
            
        def login(self, username='testuser', password='testpass'):
            return self._client.post('/login', data={
                'username': username,
                'password': password
            }, follow_redirects=True)
            
        def logout(self, clear_cart=False):
            url = '/logout/clear-cart' if clear_cart else '/logout'
            return self._client.get(url, follow_redirects=True)
    
    return AuthActions(client) 