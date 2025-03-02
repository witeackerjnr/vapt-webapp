from flask import Flask, request, jsonify
from flask_cors import CORS
import nmap3
import re
import time

app = Flask(__name__)

# Allow only Netlify frontend (Replace with your actual Netlify URL)
NETLIFY_URL = "https://webdefend.netlify.app"
CORS(app, resources={r"/scan": {"origins": NETLIFY_URL, "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}}, supports_credentials=True)

# Rate limiting dictionary
request_count = {}

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the VAPT Web App!"}), 200

def run_nmap_scan(target):
    """Runs a basic Nmap scan using python-nmap3."""
    nm = nmap3.NmapScanTechniques()
    try:
        scan_result = nm.nmap_ping_scan(target)
        return scan_result
    except Exception as e:
        return {"error": f"Nmap error: {str(e)}"}

@app.route("/scan", methods=["POST", "OPTIONS"])
def scan():
    """Handles scanning requests from the frontend."""
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS Preflight OK"}), 200

    data = request.json
    target = data.get("target")

    if not target:
        return jsonify({"error": "Target IP/Domain is required"}), 400

    if not re.match(r"^(?:[a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+$", target):
        return jsonify({"error": "Invalid target format"}), 400

    scan_result = run_nmap_scan(target)
    
    return jsonify({"scan_result": scan_result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)
