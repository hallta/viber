"""
WSGI entry point for the Viber application.
"""

from viber import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=8080) 