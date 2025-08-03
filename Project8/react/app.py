from flask import Flask, render_template, request
import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Additional imports for HTTP server and authentication
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json, os, bcrypt, urllib.parse

# Flask app setup
app = Flask(__name__)

# Load and prepare the ML model
df = pd.read_csv("crop_recommendation.csv")
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']
le = LabelEncoder()
y_encoded = le.fit_transform(y)

model = RandomForestClassifier()
model.fit(X, y_encoded)

# DB connection
conn = sqlite3.connect('agri1.db', check_same_thread=False)
conn.execute('''CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    N REAL, P REAL, K REAL, temperature REAL, humidity REAL, ph REAL, rainfall REAL, crop TEXT)''')
conn.commit()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    result = []
    if request.method == "POST":
        try:
            data = [float(request.form[key]) for key in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
            input_array = np.array([data])
            
            # Get only the most probable crop
            pred = model.predict(input_array)
            crop = le.inverse_transform(pred)[0]

            # Save the predicted crop in DB
            conn.execute("INSERT INTO predictions (N, P, K, temperature, humidity, ph, rainfall, crop) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (*data, crop))
            conn.commit()

            result = [crop]
        except Exception as e:
            result = [f"Error: {str(e)}"]
    return render_template("recommend.html", result=result)

@app.route("/about")
def about():
    return render_template("about.html")

# --- HTTP Server and Auth Handler for signup/login ---

PORT = 8080
USERS_FILE = "users.json"

class AuthHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        fields = urllib.parse.parse_qs(post_data.decode('utf-8'))

        if self.path == "/signup":
            username = fields.get('username', [''])[0]
            password = fields.get('password', [''])[0]
            self.signup_user(username, password)

        elif self.path == "/login":
            username = fields.get('username', [''])[0]
            password = fields.get('password', [''])[0]
            self.login_user(username, password)

    def signup_user(self, username, password):
        users = self.load_users()

        if username in users:
            self.respond("Username already exists. Try logging in.")
            return

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        users[username] = hashed_pw
        self.save_users(users)

        self.respond("<h2>Signup successful!</h2><a href='/templates/login.html'>Login</a>")

    def login_user(self, username, password):
        users = self.load_users()

        if username in users and bcrypt.checkpw(password.encode(), users[username].encode()):
            self.respond(open('templates/welcome.html').read())
        else:
            self.respond("<h2>Login failed!</h2><a href='/templates/login.html'>Try Again</a>")

    def respond(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if "<html>" not in message:
            message = f"<html><body>{message}</body></html>"
        self.wfile.write(message.encode())

    def load_users(self):
        if not os.path.exists(USERS_FILE):
            return {}
        with open(USERS_FILE, 'r') as f:
            return json.load(f)

    def save_users(self, users):
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f)

    def do_GET(self):
        if self.path == "/":
            self.path = "/templates/signup.html"
        return super().do_GET()

if __name__ == "__main__":
    # Start Flask app in debug mode
    from threading import Thread

    def run_flask():
        app.run(debug=True, use_reloader=False)

    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start HTTP server for authentication
    os.chdir('.')  # Set base directory
    server = HTTPServer(('', PORT), AuthHandler)
    print(f"Server started on http://localhost:{PORT}")
    server.serve_forever()
