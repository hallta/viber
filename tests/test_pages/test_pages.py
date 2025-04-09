"""
Tests for page functionality.
"""

def test_public_pages_accessible(client):
    """Test that public pages are accessible without authentication."""
    public_routes = ['/', '/about', '/contact', '/products']
    
    for route in public_routes:
        # Without login
        response = client.get(route)
        assert response.status_code == 200
        
        # With login
        with client.session_transaction() as sess:
            sess['authenticated'] = True
            sess['username'] = 'testuser'
        response = client.get(route)
        assert response.status_code == 200

def test_products_page_accessible(client):
    """Test that products page is accessible without login."""
    response = client.get('/products')
    assert response.status_code == 200
    assert b'Our Hat Collection' in response.data
    assert b'Test Hat' in response.data
    assert b'$29.99' in response.data

def test_products_page_content(client):
    """Test that products page displays all required elements."""
    response = client.get('/products')
    assert b'card-img-top' in response.data  # Image element
    assert b'card-title' in response.data    # Title element
    assert b'card-text' in response.data     # Description element
    assert b'badge' in response.data         # Category badge
    assert b'Add to Cart' in response.data   # Add to cart button

def test_navigation_includes_products(client):
    """Test that navigation bar includes products link."""
    response = client.get('/about')  # Use public page
    assert b'href="/products"' in response.data
    assert b'Products' in response.data 