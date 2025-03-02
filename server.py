from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import re
import time

app = Flask(__name__)
CORS(app, resources={r"/scan": {"origins": "https://webdefend.netlify.app/"}})

# Rate limiting dictionary
request_count = {}

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the VAPT Web App!"}), 200

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    target = data.get("target")

    if not target:
        return jsonify({"error": "Target IP/Domain is required"}), 400

    # Prevent command injection by allowing only IPs or domains
    if not re.match(r"^[a-zA-Z0-9.-]+$", target):
        return jsonify({"error": "Invalid target format"}), 400

    # Rate Limiting (Allow max 3 requests per 10 seconds)
    client_ip = request.remote_addr
    current_time = time.time()

    if client_ip in request_count:
        last_request_time = request_count[client_ip]
        if current_time - last_request_time < 10:
            return jsonify({"error": "Too many requests. Please wait."}), 429

    request_count[client_ip] = current_time

    # Run Nmap scan
    result = subprocess.run(["nmap", "-F", target], capture_output=True, text=True)

    return jsonify({"scan_result": result.stdout}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)
