#!/bin/bash

# Navigate to the directory containing the Flask app
cd "$(dirname "$0")"

# Activate the Python virtual environment
source venv/bin/activate

# Export Flask environment variables
export FLASK_APP=app.py
export FLASK_ENV=production  # Change to "development" if needed

# Start the Flask app with the full path to flask
$(pwd)/venv/bin/flask run --host=0.0.0.0 --port=5000