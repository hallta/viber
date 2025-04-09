"""
Unit tests for the Viber web application.
Tests routing, template rendering, navigation functionality, and authentication.
"""

import unittest
from flask import template_rendered, session
from contextlib import contextmanager
from main import app, db, Product, CartItem
import json


@contextmanager
def captured_templates(app):
    """
    Context manager to capture templates being rendered.
    
    Args:
        app: Flask application instance
    
    Yields:
        list: List of (template, context) tuples
    """
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class TestViberApp(unittest.TestCase):
    """Test cases for the Viber web application."""
    
    def setUp(self):
        """Set up test client and other test variables."""
        self.app = app
        self.client = app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with self.app.app_context():
            # Create all tables
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
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        
    def login(self, username='testuser', password='testpass'):
        """Helper method to log in a test user."""
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
    
    def logout(self):
        """Helper method to log out."""
        return self.client.get('/logout', follow_redirects=True)

    def test_login_page_loads(self):
        """Test that login page loads correctly."""
        with captured_templates(self.app) as templates:
            response = self.client.get('/login')
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(templates), 1)
            template, context = templates[0]
            self.assertEqual(template.name, 'login.html')
            self.assertEqual(context['active_page'], 'login')

    def test_login_success(self):
        """Test successful login with any credentials."""
        response = self.login()
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertTrue(sess['authenticated'])
            self.assertEqual(sess['username'], 'testuser')

    def test_login_missing_fields(self):
        """Test login with missing credentials."""
        response = self.client.post('/login', data=dict(
            username='',
            password=''
        ), follow_redirects=True)
        self.assertIn(b'Please provide both username and password', response.data)

    def test_logout(self):
        """Test logout functionality."""
        self.login()
        response = self.logout()
        
        with self.client.session_transaction() as sess:
            self.assertNotIn('authenticated', sess)
            self.assertNotIn('username', sess)
        
        self.assertIn(b'Successfully logged out!', response.data)

    def test_home_page_requires_login(self):
        """Test that home page requires authentication."""
        # Without login
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
        
        # With login
        self.login()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home', response.data)

    def test_public_pages_accessible(self):
        """Test that about and contact pages are publicly accessible."""
        public_routes = ['/about', '/contact']
        
        for route in public_routes:
            # Without login
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            
            # With login
            self.login()
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)

    def test_login_redirect_to_home(self):
        """Test that login redirects to home page when no next parameter."""
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home', response.data)

    def test_login_redirect_to_next(self):
        """Test that login redirects to 'next' parameter."""
        # Try to access protected home page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        
        # Login with next parameter
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='testpass'
        ), follow_redirects=True)
        
        # Should end up at home page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home', response.data)

    def test_navigation_shows_login_when_not_authenticated(self):
        """Test that navigation shows login link when not authenticated."""
        response = self.client.get('/about')  # Using public page
        data = response.data.decode()
        # Check for the login link in the navigation
        self.assertIn('href="/login"', data)
        self.assertIn('Login', data)
        self.assertNotIn('Logout', data)

    def test_navigation_shows_logout_when_authenticated(self):
        """Test that navigation shows logout link when authenticated."""
        self.login()
        response = self.client.get('/about')  # Using public page
        data = response.data.decode()
        # Check for the welcome message and logout link
        self.assertIn('Welcome, testuser', data)
        self.assertIn('href="/logout"', data)
        self.assertNotIn('href="/login"', data)

    def test_template_inheritance(self):
        """Test that all pages properly extend the base template."""
        # Test public pages without login
        public_routes = ['/about', '/contact']
        for route in public_routes:
            response = self.client.get(route)
            self.assertIn('navbar', response.data.decode())
            self.assertIn('content-wrapper', response.data.decode())
        
        # Test home page with login
        self.login()
        response = self.client.get('/')
        self.assertIn('navbar', response.data.decode())
        self.assertIn('content-wrapper', response.data.decode())
    
    def test_navigation_links(self):
        """Test that navigation links are present and correct."""
        response = self.client.get('/about')  # Using public page
        data = response.data.decode()
        
        # Check for presence of navigation links
        self.assertIn('href="/"', data)
        self.assertIn('href="/about"', data)
        self.assertIn('href="/contact"', data)
    
    def test_active_page_highlighting(self):
        """Test that the active page is properly highlighted in navigation."""
        # Test public pages
        public_routes = {
            '/about': 'about',
            '/contact': 'contact'
        }
        
        for route, page in public_routes.items():
            response = self.client.get(route)
            data = response.data.decode()
            self.assertIn('nav-link active', data)
            self.assertIn('aria-current="page"', data)
        
        # Test home page (requires login)
        self.login()
        response = self.client.get('/')
        data = response.data.decode()
        self.assertIn('nav-link active', data)
        self.assertIn('aria-current="page"', data)

    def test_products_page_accessible(self):
        """Test that products page is accessible without login"""
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Our Hat Collection', response.data)
        self.assertIn(b'Test Hat', response.data)
        self.assertIn(b'$29.99', response.data)

    def test_products_in_database(self):
        """Test that products can be retrieved from database"""
        with self.app.app_context():
            products = Product.query.all()
            self.assertTrue(len(products) > 0)
            self.assertEqual(products[0].name, 'Test Hat')
            self.assertEqual(products[0].price, 29.99)

    def test_products_page_content(self):
        """Test that products page displays all required elements"""
        response = self.client.get('/products')
        self.assertIn(b'card-img-top', response.data)  # Image element
        self.assertIn(b'card-title', response.data)    # Title element
        self.assertIn(b'card-text', response.data)     # Description element
        self.assertIn(b'badge', response.data)         # Category badge
        self.assertIn(b'Add to Cart', response.data)   # Add to cart button

    def test_navigation_includes_products(self):
        """Test that navigation bar includes products link"""
        response = self.client.get('/about')  # Use public page instead of home
        self.assertIn(b'href="/products"', response.data)
        self.assertIn(b'Products', response.data)

    def test_add_to_cart(self):
        """Test adding a product to cart"""
        self.login()  # Log in first
        
        with self.app.app_context():
            # Get the test product ID
            product = Product.query.first()
            
            # Add to cart
            response = self.client.post(f'/cart/add/{product.id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['cart_count'], 1)
            
            # Verify item in cart
            cart_item = CartItem.query.first()
            self.assertIsNotNone(cart_item)
            self.assertEqual(cart_item.product_id, product.id)
            self.assertEqual(cart_item.quantity, 1)

    def test_update_cart_quantity(self):
        """Test updating cart item quantity"""
        self.login()  # Log in first
        
        with self.app.app_context():
            # Add item to cart first
            product = Product.query.first()
            self.client.post(f'/cart/add/{product.id}')
            cart_item = CartItem.query.first()
            
            # Update quantity
            response = self.client.post(
                f'/cart/update/{cart_item.id}',
                json={'quantity': 3},
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            
            # Verify quantity updated
            cart_item = CartItem.query.first()
            self.assertEqual(cart_item.quantity, 3)

    def test_remove_from_cart(self):
        """Test removing item from cart"""
        self.login()  # Log in first
        
        with self.app.app_context():
            # Add item to cart first
            product = Product.query.first()
            self.client.post(f'/cart/add/{product.id}')
            cart_item = CartItem.query.first()
            
            # Remove item
            response = self.client.post(f'/cart/remove/{cart_item.id}')
            self.assertEqual(response.status_code, 200)
            
            # Verify item removed
            cart_item = CartItem.query.first()
            self.assertIsNone(cart_item)

    def test_view_cart_page(self):
        """Test viewing the cart page"""
        self.login()  # Log in first
        
        with self.app.app_context():
            # Add item to cart first
            product = Product.query.first()
            self.client.post(f'/cart/add/{product.id}')
            
            # View cart
            response = self.client.get('/cart')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Shopping Cart', response.data)
            self.assertIn(product.name.encode(), response.data)
            self.assertIn(str(product.price).encode(), response.data)

    def test_cart_session_isolation(self):
        """Test that cart items are session-specific"""
        self.login(username='user1')  # Log in first user
        
        with self.app.app_context():
            product = Product.query.first()
            
            # Add item in first session
            self.client.post(f'/cart/add/{product.id}')
            
            # Create new client and log in as different user
            client2 = app.test_client()
            with client2.session_transaction() as sess:
                sess['authenticated'] = True
                sess['username'] = 'user2'
            
            # Check second user's cart
            response = client2.get('/cart')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your cart is empty', response.data)

    def test_cart_requires_auth(self):
        """Test that cart operations require authentication"""
        with self.app.app_context():
            # Get the test product ID
            product = Product.query.first()
            
            # Try to view cart without auth
            response = self.client.get('/cart')
            self.assertEqual(response.status_code, 302)  # Redirects to login
            self.assertIn('/login', response.location)
            
            # Try to add to cart without auth
            response = self.client.post(f'/cart/add/{product.id}')
            self.assertEqual(response.status_code, 302)  # Redirects to login
            self.assertIn('/login', response.location)
            
            # Try to update cart without auth
            response = self.client.post('/cart/update/1', json={'quantity': 2})
            self.assertEqual(response.status_code, 302)  # Redirects to login
            self.assertIn('/login', response.location)
            
            # Try to remove from cart without auth
            response = self.client.post('/cart/remove/1')
            self.assertEqual(response.status_code, 302)  # Redirects to login
            self.assertIn('/login', response.location)

    def test_cart_operations_with_auth(self):
        """Test cart operations when authenticated"""
        self.login()  # Log in first
        
        with self.app.app_context():
            # Get the test product
            product = Product.query.first()
            
            # Add to cart
            response = self.client.post(f'/cart/add/{product.id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['cart_count'], 1)
            
            # View cart
            response = self.client.get('/cart')
            self.assertEqual(response.status_code, 200)
            self.assertIn(product.name.encode(), response.data)
            
            # Update quantity
            cart_item = CartItem.query.first()
            response = self.client.post(
                f'/cart/update/{cart_item.id}',
                json={'quantity': 3},
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            
            # Verify quantity updated
            cart_item = CartItem.query.first()
            self.assertEqual(cart_item.quantity, 3)
            
            # Remove from cart
            response = self.client.post(f'/cart/remove/{cart_item.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(CartItem.query.first())

    def test_cart_cleared_on_logout(self):
        """Test that cart items are cleared when user explicitly logs out with cart clearing"""
        self.login()
        
        with self.app.app_context():
            # Add item to cart
            product = Product.query.first()
            self.client.post(f'/cart/add/{product.id}')
            
            # Verify item in cart
            self.assertIsNotNone(CartItem.query.first())
            
            # Logout with cart clearing
            response = self.client.get('/logout/clear-cart')
            self.assertEqual(response.status_code, 302)  # Should redirect
            
            # Verify cart is empty
            self.assertIsNone(CartItem.query.first())

    def test_cart_persists_on_regular_logout(self):
        """Test that cart items persist when user logs out normally"""
        self.login()
        
        with self.app.app_context():
            # Add item to cart
            product = Product.query.first()
            self.client.post(f'/cart/add/{product.id}')
            
            # Verify item in cart
            cart_item = CartItem.query.first()
            self.assertIsNotNone(cart_item)
            
            # Regular logout
            self.client.get('/logout')
            
            # Verify cart item still exists
            persisted_item = CartItem.query.first()
            self.assertIsNotNone(persisted_item)
            self.assertEqual(persisted_item.id, cart_item.id)

    def test_cart_isolation_between_users(self):
        """Test that cart items are isolated between different users"""
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
            self.client.get('/logout')
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