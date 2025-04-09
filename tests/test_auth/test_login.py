"""
Tests for authentication functionality.
"""

from flask import session, template_rendered
from contextlib import contextmanager

@contextmanager
def captured_templates(app):
    """Context manager to capture templates being rendered."""
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

def test_login_page_loads(app, client):
    """Test that login page loads correctly."""
    with captured_templates(app) as templates:
        response = client.get('/login')
        
        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'login.html'
        assert context['active_page'] == 'login'

def test_login_success(client):
    """Test successful login with any credentials."""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert sess['authenticated']
        assert sess['username'] == 'testuser'

def test_login_missing_fields(client):
    """Test login with missing credentials."""
    response = client.post('/login', data={
        'username': '',
        'password': ''
    }, follow_redirects=True)
    assert b'Please provide both username and password' in response.data

def test_login_redirect_to_home(client):
    """Test that login redirects to home page when no next parameter."""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Home' in response.data

def test_login_redirect_to_next(client):
    """Test that login redirects to 'next' parameter."""
    # Try to access protected cart page
    response = client.get('/cart')
    assert response.status_code == 302
    assert response.location == '/login?next=/cart'
    
    # Login with next parameter from the redirect URL
    response = client.post('/login?next=/cart', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=False)
    
    # Should redirect to cart page
    assert response.status_code == 302
    assert response.location == '/cart'
    
    # Follow redirect to cart page
    response = client.get(response.location, follow_redirects=True)
    assert response.status_code == 200
    assert b'Shopping Cart' in response.data

def test_logout(auth, client):
    """Test logout functionality."""
    auth.login()
    response = auth.logout()
    
    with client.session_transaction() as sess:
        assert 'authenticated' not in sess
        assert 'username' not in sess
    
    assert b'Successfully logged out!' in response.data

def test_navigation_shows_login_when_not_authenticated(client):
    """Test that navigation shows login link when not authenticated."""
    response = client.get('/about')  # Using public page
    data = response.data.decode()
    # Check for the login link in the navigation
    assert 'href="/login"' in data
    assert 'Login' in data
    assert 'Logout' not in data

def test_navigation_shows_logout_when_authenticated(auth, client):
    """Test that navigation shows logout link when authenticated."""
    auth.login()
    response = client.get('/about')  # Using public page
    data = response.data.decode()
    # Check for the welcome message and logout link
    assert 'Welcome, testuser' in data
    assert 'href="/logout"' in data
    assert 'href="/login"' not in data 