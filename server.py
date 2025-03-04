from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import re

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    """Ensure all responses include proper CORS headers"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the VAPT Web App!"}), 200

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    target = data.get("target")

    if not target:
        return jsonify({"error": "Target IP/Domain is required"}), 400

    if not re.match(r"^[a-zA-Z0-9.-]+$", target):
        return jsonify({"error": "Invalid target format"}), 400

    try:
        # Run Nmap with `-F --unprivileged` mode (as you requested)
        result = subprocess.run(
            ["nmap", "-F", "--unprivileged", target], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        full_output = result.stdout + result.stderr  # Combine stdout & stderr
        return jsonify({"scan_result": full_output}), 200
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Scan timed out. Try again later."}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
