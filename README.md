# SRT Relay Project w/Control Panel

This project sets up an SRT relay server using Flask and `srt-live-transmit`.

## Features
- Start and stop SRT relays via a web interface.
- Optional passphrase encryption for SRT streams.
- Lightweight and easy to install.

## Prerequisites
- Ubuntu/Debian-based system
- Python 3.8 or higher
- `srt` library installed

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/srt-relay.git
   cd srt-relay
   ```
2. Run the setup script:
    ```bash
    Copiar código
    ./setup.sh
    ```
3. Start the Flask app:

    ```bash
    Copiar código
    ./start.sh
    ```
4. Access the web interface:

    Open your browser and navigate to `http://<your-server-ip>:5000`.
