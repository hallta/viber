# Viber

A Flask web application featuring a hat store with authentication, product catalog, shopping cart, and responsive design.

## Features

- User authentication system
- Shopping cart functionality with user isolation
- Responsive navigation bar
- Product catalog with database integration
- Bootstrap-based UI
- Flash messages for user feedback
- Session management
- Mobile-friendly design
- SQLite database for product and cart management
- Docker support for containerized deployment

## Getting Started

### Prerequisites
- Python 3.x
- pip (Python package installer)
- SQLite3 (included with Python)
- Docker (optional, for containerized deployment)

### Setup

1. Create and activate the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies and the package in development mode:
```bash
pip install -r requirements.txt
pip install -e .
```

3. Initialize the database with sample data:
```bash
PYTHONPATH=/path/to/viber python src/viber/init_db.py
```
This will:
- Create the instance directory if it doesn't exist
- Create all necessary database tables
- Add 100 sample products with diverse attributes
- Set up the SQLite database in the instance directory

### Running the Server

There are two ways to run the server:

#### Method 1: Using Flask CLI
```bash
PYTHONPATH=/path/to/viber FLASK_APP=src.viber:create_app FLASK_ENV=development flask run --port 8080
```

#### Method 2: Using Python
```bash
PYTHONPATH=/path/to/viber python wsgi.py
```

The server will start on `http://localhost:8080`. You can visit this URL in your web browser.

Note: Port 8080 is used to avoid conflicts with macOS AirPlay Receiver service which uses port 5000.

## Authentication

The application implements a basic authentication system:

### Features
- Public access to Home, About, Contact, and Products pages
- Protected cart functionality requiring login
- Session-based authentication
- Automatic redirect to login page when accessing protected routes
- "Remember where you came from" - redirects back to originally requested page after login
- Cart persistence across sessions
- Option to clear cart on logout

### Usage
1. All main pages (Home, About, Contact, Products) are publicly accessible
2. Adding items to cart or viewing cart requires authentication
3. Enter any username and password (all credentials are accepted in this version)
4. After login, you'll be redirected to your original destination
5. Use the regular logout to preserve your cart items
6. Use "Logout & Clear Cart" to remove all items from your cart

## Shopping Cart

The application includes a full-featured shopping cart system:

### Features
- Add products to cart
- Update quantities
- Remove items
- Cart total calculation
- Cart persistence across sessions
- User-isolated carts
- Cart count badge in navigation
- AJAX updates for smooth user experience

### Database Schema
The cart_items table includes:
- id (Primary Key)
- session_id (String, links to user)
- product_id (Integer, Foreign Key to products)
- quantity (Integer)
- created_at (DateTime)

## Product Catalog

The application includes a product catalog system:

### Features
- SQLite database integration
- Responsive product grid layout
- Product categories with diverse attributes
- Price display
- Product images
- Add to cart functionality
- Stock management

### Database Schema
The products table includes:
- id (Primary Key)
- name (String)
- description (Text)
- price (Float)
- image_url (String)
- category (String) - T-Shirts, Shirts, Pants, etc.
- fit (String) - Regular, Slim, Relaxed, etc.
- size (String) - XS, S, M, L, XL, XXL
- color (String) - Black, White, Navy, etc.
- material (String) - Cotton, Polyester, Wool, etc.
- style (String) - Casual, Formal, Sport, etc.
- season (String) - Spring, Summer, Fall, Winter, All-Season
- gender (String) - Men, Women, Unisex
- in_stock (Boolean)
- stock_quantity (Integer)
- created_at (DateTime)
- updated_at (DateTime)

## Testing

The project includes a comprehensive test suite using pytest. Here's how to run the tests:

### Running All Tests
```bash
# Run all tests with coverage report
pytest

# Run tests with verbose output
pytest -v
```

### Running Specific Tests
```bash
# Run tests in a specific file
pytest tests/test_auth/test_login.py

# Run tests matching a pattern
pytest -k "test_login"

# Run tests in a specific directory
pytest tests/test_auth/
```

### Test Coverage
The test suite includes coverage reporting. When you run `pytest`, it will automatically:
- Run all tests
- Generate a coverage report showing which lines of code were executed
- Display any failing tests with detailed output

### Understanding Test Output
- Green dots (.) indicate passing tests
- 'F' indicates a failing test
- 'E' indicates an error during test execution
- The final summary shows:
  - Number of tests run
  - Number of failures/errors
  - Test coverage percentage
  - Time taken to run tests

### Troubleshooting Tests
If tests fail, make sure:
1. You've installed the package in development mode (`pip install -e .`)
2. All dependencies are installed (`pip install -r requirements.txt`)
3. You're running tests from the project root directory
4. Your virtual environment is activated

## Project Structure

```
viber/
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── instance/               # Instance directory for SQLite database
│   └── viber.db           # SQLite database
├── src/                    # Source code directory
│   └── viber/             # Main package directory
│       ├── __init__.py    # Application factory
│       ├── extensions.py  # Flask extensions
│       ├── init_db.py     # Database initialization script
│       ├── models/        # Database models
│       │   ├── product.py # Product model
│       │   └── cart.py    # Cart model
│       ├── routes/        # Route blueprints
│       │   ├── auth.py    # Authentication routes
│       │   ├── cart.py    # Cart routes
│       │   └── pages.py   # Page routes
│       └── utils/         # Utility functions
├── templates/              # HTML templates directory
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Home page template
│   ├── about.html         # About page template
│   ├── contact.html       # Contact page template
│   ├── products.html      # Products page template
│   └── cart.html          # Cart page template
└── static/                # Static files directory
    ├── css/              # CSS files
    └── js/               # JavaScript files
```

## Contributing

Guidelines for contributing will be added as the project matures.

## License

This project's license information will be added soon. 