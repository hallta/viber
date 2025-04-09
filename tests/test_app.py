"""
Integration tests for the Viber application.
"""

import unittest
from flask import session
from viber import create_app, db
from viber.models.product import Product
from viber.models.cart import CartItem

class TestApp(unittest.TestCase):
    def setUp(self):
        """Set up test application."""
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'WTF_CSRF_ENABLED': False
        })
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
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

    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username='testuser', password='testpass'):
        """Helper method to log in."""
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self, clear_cart=False):
        """Helper method to log out."""
        url = '/logout/clear-cart' if clear_cart else '/logout'
        return self.client.get(url, follow_redirects=True)

    def test_public_pages_accessible(self):
        """Test that public pages are accessible without authentication."""
        public_routes = ['/', '/about', '/contact', '/products']
        
        for route in public_routes:
            # Without login
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            
            # With login
            with self.client.session_transaction() as sess:
                sess['authenticated'] = True
                sess['username'] = 'testuser'
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)

    def test_login_redirect_to_next(self):
        """Test that login redirects to 'next' parameter."""
        # Try to access protected cart page
        response = self.client.get('/cart')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/login?next=/cart')
        
        # Login with next parameter from the redirect URL
        response = self.client.post('/login?next=/cart', data=dict(
            username='testuser',
            password='testpass'
        ), follow_redirects=False)
        
        # Should redirect to cart page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/cart')
        
        # Follow redirect to cart page
        response = self.client.get(response.location, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Shopping Cart', response.data)

    def test_cart_isolation_between_users(self):
        """Test that cart items are isolated between different users."""
        with self.app.app_context():
            product = Product.query.first()
            
            # First user adds item
            self.login(username='user1')
            self.client.post(f'/cart/add/{product.id}')
            
            # Verify first user's cart
            cart_items = CartItem.query.filter_by(session_id='user1').all()
            self.assertEqual(len(cart_items), 1)
            self.assertEqual(cart_items[0].product_id, product.id)
            
            # Switch to second user (using regular logout to preserve cart items)
            self.logout()
            self.login(username='user2')
            
            # Add same item to second user's cart
            self.client.post(f'/cart/add/{product.id}')
            
            # Verify both users have their own cart items
            user1_items = CartItem.query.filter_by(session_id='user1').all()
            user2_items = CartItem.query.filter_by(session_id='user2').all()
            
            self.assertEqual(len(user1_items), 1, "User1 should have 1 item")
            self.assertEqual(len(user2_items), 1, "User2 should have 1 item")
            self.assertEqual(user1_items[0].product_id, product.id)
            self.assertEqual(user2_items[0].product_id, product.id)
            self.assertNotEqual(user1_items[0].id, user2_items[0].id)

if __name__ == '__main__':
    unittest.main() 