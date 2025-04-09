"""
Setup configuration for the Viber application.
"""

from setuptools import setup, find_packages

setup(
    name="viber",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "Flask>=3.0.0",
        "Werkzeug>=3.0.1",
        "Flask-SQLAlchemy>=3.1.1",
        "SQLAlchemy>=2.0.25",
        "Flask-WTF>=1.2.1",
        "WTForms>=3.1.1",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.8",
) 