import random
import string
from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)
process = None  # Variable to store the process ID
stream_id = None  # Global variable for the stream ID


def generate_stream_id():
    """Generate a random stream ID with optional metadata."""
    unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return f"streamid={unique_id}"


@app.route("/")
def index():
    """Serve the frontend."""
    global stream_id
    if stream_id is None:  # Generate a stream ID if not already set
        stream_id = generate_stream_id()
    return render_template("index.html", stream_id=stream_id)


@app.route("/get_stream_id", methods=["GET"])
def get_stream_id():
    """Get the current stream ID."""
    return jsonify({"stream_id": stream_id})


@app.route("/regenerate_stream_id", methods=["POST"])
def regenerate_stream_id():
    """Regenerate the stream ID."""
    global stream_id
    stream_id = generate_stream_id()
    return jsonify({"stream_id": stream_id})


@app.route("/start", methods=["POST"])
def start_relay():
    """Start the SRT relay."""
    global process, stream_id
    if process:
        return jsonify({"error": "Relay already running"}), 400

    data = request.json
    sender_port = data["sender_port"]
    receiver_port = data["receiver_port"]
    user_stream_id = data.get("stream_id", stream_id)  # Use user-provided or current stream ID

    # Build the SRT URLs with the stream ID
    sender_url = f"srt://0.0.0.0:{sender_port}?mode=listener&{user_stream_id}"
    receiver_url = f"srt://0.0.0.0:{receiver_port}?mode=listener&{user_stream_id}"

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
