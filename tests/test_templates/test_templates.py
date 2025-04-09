"""
Tests for template functionality.
"""

def test_template_inheritance(client):
    """Test that all pages properly extend the base template."""
    response = client.get('/')
    assert response.status_code == 200
    
    # Check for key elements of base template
    content = response.data.decode()
    assert 'navbar' in content  # Navigation bar
    assert 'flex-shrink-0' in content  # Main content wrapper
    assert 'footer' in content  # Footer
    assert 'container' in content  # Bootstrap container

def test_navigation_links(client):
    """Test that navigation links are present and correct."""
    response = client.get('/about')  # Using public page
    data = response.data.decode()
    
    # Check for presence of navigation links
    assert 'href="/"' in data
    assert 'href="/about"' in data
    assert 'href="/contact"' in data

def test_active_page_highlighting(auth, client):
    """Test that the active page is properly highlighted in navigation."""
    # Test public pages
    public_routes = {
        '/': 'home',
        '/about': 'about',
        '/contact': 'contact',
        '/products': 'products'
    }
    
    for route, page in public_routes.items():
        response = client.get(route)
        data = response.data.decode()
        assert 'nav-link active' in data
        assert 'aria-current="page"' in data
    
    # Test protected cart page
    auth.login()
    response = client.get('/cart')
    data = response.data.decode()
    assert 'nav-link active' in data
    assert 'aria-current="page"' in data 