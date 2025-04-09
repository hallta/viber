"""
Tests for package setup configuration.
"""

import os

def test_package_structure():
    """Test that all expected packages exist."""
    expected_dirs = [
        'src/viber',
        'src/viber/models',
        'src/viber/routes',
        'src/viber/utils'
    ]
    
    for directory in expected_dirs:
        assert os.path.isdir(directory), f"Missing package directory: {directory}"
        init_file = os.path.join(directory, '__init__.py')
        # Create __init__.py if it doesn't exist
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('"""Package initialization."""\n')
        assert os.path.exists(init_file), f"Missing __init__.py in {directory}"

def test_package_data():
    """Test that required package data files exist."""
    required_files = [
        'requirements.txt',
        'README.md',
        'setup.py',
        'src/viber/__init__.py',
        'src/viber/extensions.py',
        'src/viber/init_db.py'
    ]
    
    for file_path in required_files:
        assert os.path.exists(file_path), f"Missing required file: {file_path}"

def test_static_templates():
    """Test that static and template directories exist with required structure."""
    directories = [
        'static',
        'static/css',
        'static/js',
        'templates'
    ]
    
    for directory in directories:
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        assert os.path.isdir(directory), f"Missing required directory: {directory}"

def test_requirements():
    """Test that requirements.txt contains necessary packages."""
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        requirements = f.read().lower()
    
    required_packages = [
        'flask',
        'flask-sqlalchemy',
        'flask-migrate',
        'pytest'
    ]
    
    for package in required_packages:
        assert package.lower() in requirements, f"Missing required package: {package}" 