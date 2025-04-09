"""
Tests for database initialization functionality.
"""

from viber import db
from viber.init_db import generate_products, generate_price, generate_description
from viber.models.product import Product, CATEGORIES, FITS, MATERIALS, STYLES

def test_generate_price():
    """Test that generate_price returns a valid price."""
    price = generate_price()
    assert isinstance(price, float)
    assert 19.99 <= price <= 199.99
    assert round(price, 2) == price  # Check that price has 2 decimal places

def test_generate_description():
    """Test that generate_description creates a valid description."""
    name = "Test Product"
    material = "Cotton"
    style = "Casual"
    fit = "Regular"
    
    description = generate_description(name, material, style, fit)
    assert isinstance(description, str)
    assert all(word.lower() in description.lower() for word in [material, style, fit])
    assert "perfect for any occasion" in description

def test_generate_products():
    """Test that generate_products creates the correct number of products with valid attributes."""
    products = generate_products(count=5)
    
    assert len(products) == 5
    for product in products:
        assert isinstance(product, Product)
        assert product.name
        assert product.description
        assert 19.99 <= product.price <= 199.99
        assert product.image_url.startswith('https://placehold.co/300x200')
        assert product.category in CATEGORIES
        assert product.fit in FITS
        assert product.material in MATERIALS
        assert product.style in STYLES
        assert isinstance(product.in_stock, bool)
        # stock_quantity defaults to 10 if not set
        assert product.stock_quantity == 10 or isinstance(product.stock_quantity, int)

def test_init_db(app):  # pylint: disable=unused-argument
    """Test database initialization with sample data."""
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Generate test products
        products = generate_products(count=5)  # Use a smaller count for testing
        db.session.bulk_save_objects(products)
        db.session.commit()
        
        # Verify products were created
        db_products = Product.query.all()
        assert len(db_products) == 5, f"Expected 5 products, got {len(db_products)}"
        
        # Check that products have all required attributes
        sample_product = db_products[0]
        assert sample_product.name, "Product name is missing"
        assert sample_product.description, "Product description is missing"
        assert sample_product.price > 0, "Invalid product price"
        assert sample_product.image_url, "Product image URL is missing"
        assert sample_product.category in CATEGORIES, f"Invalid category: {sample_product.category}"
        assert sample_product.fit in FITS, f"Invalid fit: {sample_product.fit}"
        assert sample_product.material in MATERIALS, f"Invalid material: {sample_product.material}"
        assert sample_product.style in STYLES, f"Invalid style: {sample_product.style}"
        assert isinstance(sample_product.stock_quantity, int), "Stock quantity is not an integer"
        assert sample_product.stock_quantity >= 0, "Stock quantity is negative" 