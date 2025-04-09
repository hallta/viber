# Viber

A Flask web application with authentication, navigation, and responsive design.

## Features

- User authentication system
- Responsive navigation bar
- Protected routes
- Bootstrap-based UI
- Flash messages for user feedback
- Session management
- Mobile-friendly design

## Getting Started

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Setup

1. Create and activate the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Server

1. Make sure your virtual environment is activated
2. Run the Flask application:
```bash
flask --app main run --port 8080
```

The server will start on `http://localhost:8080`. You can visit this URL in your web browser.

Note: If you see a port conflict on the default port (5000), the command above explicitly uses port 8080 to avoid conflicts with macOS AirPlay Receiver service.

## Authentication

The application implements a basic authentication system:

### Features
- Login required for all pages
- Session-based authentication
- Automatic redirect to login page
- "Remember where you came from" - redirects back to originally requested page after login

### Usage
1. Visit any page while not logged in
2. You'll be redirected to the login page
3. Enter any username and password (all credentials are accepted in this version)
4. After login, you'll be redirected to your original destination
5. Use the logout button in the navigation bar to end your session

## Testing

The project includes a comprehensive test suite using Python's unittest framework and pytest.

### Running Tests

Make sure you're in your virtual environment, then you can run tests using either pytest (recommended) or unittest:

```bash
# Using pytest (recommended)
pytest

# Using unittest
python -m unittest discover tests
```

### Test Coverage

The pytest configuration includes coverage reporting. When you run `pytest`, it will:
- Run all tests with verbose output
- Generate a coverage report
- Show which lines aren't covered by tests

### What's Being Tested

The test suite includes tests for:
- Authentication functionality
  - Login success/failure
  - Logout
  - Protected routes
  - Session management
- Route functionality for all pages
- Template rendering and context
- 404 error handling
- Template inheritance
- Navigation link presence
- Active page highlighting
- Proper template context variables

### Adding New Tests

New tests should be added to `tests/test_app.py` and should follow the existing pattern:
- Use descriptive test method names starting with `test_`
- Include docstrings explaining what is being tested
- Group related tests in test classes
- Use appropriate assertions for different types of checks

## Project Structure

```
viber/
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── main.py                # Main Flask application
├── templates/             # HTML templates directory
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page template
│   ├── about.html        # About page template
│   ├── contact.html      # Contact page template
│   └── login.html        # Login page template
├── static/               # Static files directory
│   └── css/             # CSS files directory
│       └── style.css    # Main stylesheet
├── tests/               # Test suite directory
│   ├── __init__.py     # Test package initialization
│   └── test_app.py     # Application tests
├── pytest.ini          # Pytest configuration
└── venv/               # Virtual environment directory
```

## Contributing

Guidelines for contributing will be added as the project matures.

## License

This project's license information will be added soon. 