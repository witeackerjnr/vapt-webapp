document.addEventListener("DOMContentLoaded", function() {
    // Load Navbar Dynamically
    const navbar = `
        <nav class="navbar">
            <img src="logo-placeholder.png" alt="Company Logo" class="logo">
            <ul>
                <li><a href="index.html">Home</a></li>
                <li><a href="contact.html">Contact Us</a></li>
                <li><a href="about.html">About Us</a></li>
                <li><a href="scan.html">Demo</a></li>
            </ul>
        </nav>
    `;
    document.body.insertAdjacentHTML("afterbegin", navbar);
});

// Handle Scan Form Submission
document.getElementById('scanForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const targetField = document.getElementById('target');
    const target = targetField.value.trim();
    const loading = document.getElementById('loading');
    const scanResults = document.getElementById('scanResults');

    // Clear previous results
    scanResults.innerText = "";
    loading.style.display = 'none';

    // Validate Input
    if (!target) {
        scanResults.innerText = "⚠️ Please enter a valid IP or domain.";
        return;
    }

    // Show Scanning Message Only When Scan Starts
    loading.style.display = 'block';

    try {
        const response = await fetch('https://vapt-webapp.onrender.com/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target })
        });

        const data = await response.json();

        if (response.ok) {
            scanResults.innerText = sanitizeOutput(data.scan_result);
        } else {
            scanResults.innerText = `❌ Error: ${data.error || "Unknown error"}`;
        }
    } catch (error) {
        scanResults.innerText = "❌ Failed to connect to server.";
    }

    // Hide Scanning Message When Done
    loading.style.display = 'none';
});

// Prevent XSS by escaping special characters in scan results
function sanitizeOutput(text) {
    return text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
