"""
Unit tests for the Viber web application.
Tests routing, template rendering, navigation functionality, and authentication.
"""

import unittest
from flask import template_rendered, session
from contextlib import contextmanager
from main import app


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


if __name__ == '__main__':
    unittest.main() 