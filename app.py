from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)
process = None  # Variable to store the process ID


@app.route("/")
def index():
    """Serve the frontend."""
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_relay():
    """Start the SRT relay."""
    global process
    if process:
        return jsonify({"error": "Relay already running"}), 400

    data = request.json
    sender_port = data["sender_port"]
    receiver_port = data["receiver_port"]
    sender_passphrase = data.get("sender_passphrase", "")
    receiver_passphrase = data.get("receiver_passphrase", "")

    # Build the SRT URLs with optional passphrases
    sender_url = f"srt://0.0.0.0:{sender_port}?mode=listener"
    if sender_passphrase:
        sender_url += f"&passphrase={sender_passphrase}"

    receiver_url = f"srt://0.0.0.0:{receiver_port}?mode=listener"
    if receiver_passphrase:
        receiver_url += f"&passphrase={receiver_passphrase}"

    # Start srt-live-transmit
    cmd = f"srt-live-transmit '{sender_url}' '{receiver_url}'"
    process = subprocess.Popen(cmd, shell=True)

    return jsonify({"message": "Relay started", "pid": process.pid})


@app.route("/stop", methods=["POST"])
def stop_relay():
    """Stop the SRT relay."""
    global process
    if not process:
        return jsonify({"error": "No relay is running"}), 400

    process.terminate()  # Stop the process
    process = None
    return jsonify({"message": "Relay stopped"})


@app.route("/status", methods=["GET"])
def status():
    """Check the status of the relay."""
    global process
    if process and process.poll() is None:  # Process is running
        return jsonify({"status": "running"})
    return jsonify({"status": "stopped"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)