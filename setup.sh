#!/bin/bash

# Update and install necessary system dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv srt

# Create a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Make the start script executable
chmod +x start.sh

echo "Setup complete! To start the relay, run ./start.sh"