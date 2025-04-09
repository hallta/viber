"""
Tests for cart functionality.
"""

import json
from viber.models.cart import CartItem
from viber.models.product import Product

def test_add_to_cart(auth, client, app):
    """Test adding a product to cart."""
    auth.login()  # Log in first
    
    with app.app_context():
        # Get the test product ID
        product = Product.query.first()
        
        # Add to cart
        response = client.post(f'/cart/add/{product.id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['cart_count'] == 1
        
        # Verify item in cart
        cart_item = CartItem.query.first()
        assert cart_item is not None
        assert cart_item.product_id == product.id
        assert cart_item.quantity == 1

def test_update_cart_quantity(auth, client, app):
    """Test updating cart item quantity."""
    auth.login()  # Log in first
    
    with app.app_context():
        # Add item to cart first
        product = Product.query.first()
        client.post(f'/cart/add/{product.id}')
        cart_item = CartItem.query.first()
        
        # Update quantity
        response = client.post(
            f'/cart/update/{cart_item.id}',
            json={'quantity': 3},
            content_type='application/json'
        )
        assert response.status_code == 200
        
        # Verify quantity updated
        cart_item = CartItem.query.first()
        assert cart_item.quantity == 3

def test_remove_from_cart(auth, client, app):
    """Test removing item from cart."""
    auth.login()  # Log in first
    
    with app.app_context():
        # Add item to cart first
        product = Product.query.first()
        client.post(f'/cart/add/{product.id}')
        cart_item = CartItem.query.first()
        
        # Remove item
        response = client.post(f'/cart/remove/{cart_item.id}')
        assert response.status_code == 200
        
        # Verify item removed
        cart_item = CartItem.query.first()
        assert cart_item is None

def test_view_cart_page(auth, client, app):
    """Test viewing the cart page."""
    auth.login()  # Log in first
    
    with app.app_context():
        # Add item to cart first
        product = Product.query.first()
        client.post(f'/cart/add/{product.id}')
        
        # View cart
        response = client.get('/cart')
        assert response.status_code == 200
        assert b'Shopping Cart' in response.data
        assert product.name.encode() in response.data
        assert str(product.price).encode() in response.data

def test_cart_session_isolation(auth, client, app):
    """Test that cart items are session-specific."""
    auth.login(username='user1')  # Log in first user
    
    with app.app_context():
        product = Product.query.first()
        
        # Add item in first session
        client.post(f'/cart/add/{product.id}')
        
        # Create new client and log in as different user
        client2 = app.test_client()
        with client2.session_transaction() as sess:
            sess['authenticated'] = True
            sess['username'] = 'user2'
        
        # Check second user's cart
        response = client2.get('/cart')
        assert response.status_code == 200
        assert b'Your cart is empty' in response.data

def test_cart_requires_auth(client, app):
    """Test that cart operations require authentication."""
    with app.app_context():
        # Get the test product ID
        product = Product.query.first()
        
        # Try to view cart without auth
        response = client.get('/cart')
        assert response.status_code == 302  # Redirects to login
        assert '/login' in response.location
        
        # Try to add to cart without auth
        response = client.post(f'/cart/add/{product.id}')
        assert response.status_code == 302  # Redirects to login
        assert '/login' in response.location
        
        # Try to update cart without auth
        response = client.post('/cart/update/1', json={'quantity': 2})
        assert response.status_code == 302  # Redirects to login
        assert '/login' in response.location
        
        # Try to remove from cart without auth
        response = client.post('/cart/remove/1')
        assert response.status_code == 302  # Redirects to login
        assert '/login' in response.location

def test_cart_cleared_on_logout(auth, client, app):
    """Test that cart items are cleared when user explicitly logs out with cart clearing."""
    auth.login()
    
    with app.app_context():
        # Add item to cart
        product = Product.query.first()
        client.post(f'/cart/add/{product.id}')
        
        # Verify item in cart
        assert CartItem.query.first() is not None
        
        # Logout with cart clearing
        response = auth.logout(clear_cart=True)
        assert response.status_code == 200
        
        # Verify cart is empty
        assert CartItem.query.first() is None

def test_cart_persists_on_regular_logout(auth, client, app):
    """Test that cart items persist when user logs out normally."""
    auth.login()
    
    with app.app_context():
        # Add item to cart
        product = Product.query.first()
        client.post(f'/cart/add/{product.id}')
        
        # Verify item in cart
        cart_item = CartItem.query.first()
        assert cart_item is not None
        
        # Regular logout
        auth.logout()
        
        # Verify cart item still exists
        persisted_item = CartItem.query.first()
        assert persisted_item is not None
        assert persisted_item.id == cart_item.id

def test_cart_isolation_between_users(auth, client, app):
    """Test that cart items are isolated between different users."""
    with app.app_context():
        product = Product.query.first()
        
        # First user adds item
        auth.login(username='user1')
        client.post(f'/cart/add/{product.id}')
        
        # Verify first user's cart
        cart_items = CartItem.query.filter_by(session_id='user1').all()
        assert len(cart_items) == 1
        assert cart_items[0].product_id == product.id
        
        # Switch to second user (using regular logout to preserve cart items)
        auth.logout()
        auth.login(username='user2')
        
        # Add same item to second user's cart
        client.post(f'/cart/add/{product.id}')
        
        # Verify both users have their own cart items
        user1_items = CartItem.query.filter_by(session_id='user1').all()
        user2_items = CartItem.query.filter_by(session_id='user2').all()
        
        assert len(user1_items) == 1, "User1 should have 1 item"
        assert len(user2_items) == 1, "User2 should have 1 item"
        assert user1_items[0].product_id == product.id
        assert user2_items[0].product_id == product.id
        assert user1_items[0].id != user2_items[0].id 