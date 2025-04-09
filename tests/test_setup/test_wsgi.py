"""
Tests for WSGI application configuration.
"""

from viber import create_app

def test_wsgi_app_creation():
    """Test that the WSGI application is created correctly."""
    app = create_app()
    assert app.config['SQLALCHEMY_DATABASE_URI'].endswith('viber.db')
    assert not app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
    # Check that SECRET_KEY exists and has a value
    assert app.config.get('SECRET_KEY') is not None
    assert isinstance(app.config.get('SECRET_KEY'), str)
    assert len(app.config.get('SECRET_KEY')) > 0

def test_wsgi_debug_mode():
    """Test that debug mode can be configured."""
    app = create_app({'DEBUG': True})
    assert app.debug

def test_wsgi_testing_mode():
    """Test that testing mode can be configured."""
    app = create_app({'TESTING': True})
    assert app.testing

def test_wsgi_template_paths():
    """Test that template and static paths are configured correctly."""
    app = create_app()
    assert app.template_folder.endswith('templates')
    assert app.static_folder.endswith('static')

def test_wsgi_blueprints():
    """Test that all blueprints are registered."""
    app = create_app()
    expected_blueprints = ['auth', 'cart', 'pages']
    registered_blueprints = list(app.blueprints.keys())
    
    for bp in expected_blueprints:
        assert bp in registered_blueprints, f"Missing blueprint: {bp}"
    assert len(registered_blueprints) == len(expected_blueprints), "Unexpected blueprints registered"

def test_wsgi_database_config():
    """Test database configuration."""
    test_db_uri = 'sqlite:///:memory:'
    app = create_app({
        'SQLALCHEMY_DATABASE_URI': test_db_uri
    })
    assert app.config['SQLALCHEMY_DATABASE_URI'] == test_db_uri 