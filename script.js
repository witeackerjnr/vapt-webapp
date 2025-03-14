document.addEventListener("DOMContentLoaded", function() {
    // Load Navbar Dynamically
    const navbar = `
        <nav class="navbar">
            <img src="logo-placeholder.png" alt="Company Logo" class="logo">
            <div class="hamburger" id="hamburger">
                <div></div>
                <div></div>
                <div></div>
            </div>
            <ul id="nav-links">
                <li><a href="index.html">Home</a></li>
                <li><a href="contact.html">Contact Us</a></li>
                <li><a href="about.html">About Us</a></li>
                <li><a href="scan.html">Demo</a></li>
            </ul>
        </nav>
    `;
    document.body.insertAdjacentHTML("afterbegin", navbar);

    // Mobile Navbar Toggle
    const hamburger = document.getElementById("hamburger");
    const navLinks = document.getElementById("nav-links");

    hamburger.addEventListener("click", () => {
        navLinks.classList.toggle("show");
    });
});

// Local API Base URL
const apiBaseUrl = "https://4f89-102-89-82-133.ngrok-free.app";  // Only local Flask API

console.log("Using API Base URL:", apiBaseUrl);  // Debugging

// Ensure scanForm exists before adding event listener
const scanForm = document.getElementById('scanForm');
if (scanForm) {
    scanForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const targetField = document.getElementById('target');
        const target = targetField.value.trim();
        const loading = document.getElementById('loading');
        const scanResults = document.getElementById('scanResults');

        // Clear previous results
        scanResults.innerHTML = "";
        loading.style.display = 'none';

        // Validate Input
        if (!target) {
            scanResults.innerHTML = "<span style='color: red; font-weight: bold;'>⚠️ Please enter a valid IP or domain.</span>";
            return;
        }

        // Show Scanning Message Directly Under Button
        loading.style.display = 'block';

        try {
            console.log("Sending request to:", `${apiBaseUrl}/scan`);  // Debugging

            const response = await fetch(`${apiBaseUrl}/scan`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target })
            });

            const data = await response.json();

            if (response.ok) {
                scanResults.innerHTML = formatScanResults(data.scan_result);
            } else {
                scanResults.innerHTML = `<span style='color: red; font-weight: bold;'>❌ Error: ${data.error || "Unknown error"}</span>`;
            }
        } catch (error) {
            console.error("Fetch Error:", error);  // Debugging
            scanResults.innerHTML = "<span style='color: red; font-weight: bold;'>❌ Failed to connect to server.</span>";
        }

        // Hide Scanning Message When Done
        loading.style.display = 'none';
    });
} else {
    console.error("❌ scanForm not found! Check if scan.html is loaded before script.js");
}

// Format scan results properly (prevents XSS)
function formatScanResults(text) {
    return `<pre style="background: #f4f4f4; padding: 10px; border-radius: 5px;">${text.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</pre>`;
}
