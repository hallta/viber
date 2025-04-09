# Viber

A simple Flask web server that serves a "hello world" page.

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

The server will start on `http://localhost:8080`. You can visit this URL in your web browser to see the "hello world" message.

Note: If you see a port conflict on the default port (5000), the command above explicitly uses port 8080 to avoid conflicts with macOS AirPlay Receiver service.

## Project Structure

```
viber/
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── main.py                # Main Flask application
├── templates/             # HTML templates directory
│   └── index.html        # Main page template
├── static/               # Static files directory
│   └── css/             # CSS files directory
│       └── style.css    # Main stylesheet
└── venv/                 # Virtual environment directory
```

## Contributing

Guidelines for contributing will be added as the project matures.

## License

This project's license information will be added soon. 