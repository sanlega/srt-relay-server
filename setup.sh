#!/bin/bash

# Update the system and install dependencies
sudo apt update
sudo apt upgrade -y
sudo apt install -y software-properties-common python3 python3-pip python3-venv git build-essential cmake pkg-config libssl-dev

# Install SRT tools (build from source)
if ! command -v srt-live-transmit &> /dev/null; then
  echo "SRT tools not found. Installing..."
  git clone https://github.com/Haivision/srt.git
  cd srt
  mkdir -p build && cd build
  cmake .. && make -j$(nproc)
  sudo make install
  cd ../..
  rm -rf srt
else
  echo "SRT tools are already installed."
fi

# Create a Python virtual environment
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
else
  echo "Virtual environment already exists."
fi

# Activate the virtual environment and install Python dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Make the start script executable
chmod +x start.sh

echo "Setup complete! To start the relay, run ./start.sh"
