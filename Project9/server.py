from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os

PORT = 8080
USERS_FILE = "users.txt"
COOKIE_FILE = "cookie.txt"

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.serve_file("html/index.html")
        elif self.path == "/login":
            self.serve_file("html/login.html")
        elif self.path == "/signup":
            self.serve_file("html/signup.html")
        elif self.path == "/welcome":
            if os.path.exists(COOKIE_FILE):
                self.serve_file("html/welcome.html")
            else:
                self.redirect("/login")
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode())

        if self.path == "/login":
            username = data.get("username", [None])[0]
            password = data.get("password", [None])[0]
            if self.validate_user(username, password):
                with open(COOKIE_FILE, 'w') as f:
                    f.write(username)
                self.redirect("/welcome")
            else:
                self.respond("Login failed. <a href='/login'>Try again</a>.")

        elif self.path == "/signup":
            username = data.get("username", [None])[0]
            password = data.get("password", [None])[0]
            if username and password:
                with open(USERS_FILE, 'a') as f:
                    f.write(f"{username}:{password}\n")
                self.respond("Signup successful. <a href='/login'>Login now</a>.")
            else:
                self.respond("Signup failed. <a href='/signup'>Try again</a>.")

    def validate_user(self, username, password):
        if not os.path.exists(USERS_FILE):
            return False
        with open(USERS_FILE, 'r') as f:
            for line in f:
                u, p = line.strip().split(":")
                if u == username and p == password:
                    return True
        return False

    def serve_file(self, filepath):
        if os.path.exists(filepath):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "File not found")

    def respond(self, html):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def redirect(self, location):
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

httpd = HTTPServer(('localhost', PORT), SimpleHandler)
print(f"Server started on http://localhost:{PORT}")
httpd.serve_forever()
