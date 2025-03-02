from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import re
import time

app = Flask(__name__)

# Allow only Netlify frontend 
NETLIFY_URL = "https://webdefend.netlify.app"
CORS(app, resources={r"/scan": {"origins": NETLIFY_URL, "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}}, supports_credentials=True)

# Rate limiting dictionary
request_count = {}

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the VAPT Web App!"}), 200

@app.route("/scan", methods=["POST", "OPTIONS"])
def scan():
    # Handle CORS Preflight Requests
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS Preflight OK"}), 200

    data = request.json
    target = data.get("target")

    if not target:
        return jsonify({"error": "Target IP/Domain is required"}), 400

    # Strict input validation (Only valid IPs or domains)
    if not re.match(r"^(?:[a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+$", target):
        return jsonify({"error": "Invalid target format"}), 400

    # Rate Limiting: Max 3 requests per 10 seconds per IP
    client_ip = request.remote_addr
    current_time = time.time()

    if client_ip in request_count:
        last_request_time = request_count[client_ip][0]
        request_count[client_ip] = (current_time, request_count[client_ip][1] + 1)

        if request_count[client_ip][1] > 3 and (current_time - last_request_time < 10):
            return jsonify({"error": "Too many requests. Please wait."}), 429
    else:
        request_count[client_ip] = (current_time, 1)

    # Run Secure Nmap Scan
    try:
        result = subprocess.run(["nmap", "-F", target], capture_output=True, text=True, timeout=10)
        return jsonify({"scan_result": result.stdout}), 200
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Scan timed out. Try again later."}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)
