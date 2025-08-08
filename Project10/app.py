from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd
import sqlite3
import os
from model import load_model
import auth

# Flask config
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Load model & init user table
model = load_model()
auth.create_user_table()

# ----------------------- Routes -----------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.register_user(username, password):
            return redirect('/login')
        else:
            return "Username already exists!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.login_user(username, password):
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid username or password."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('logout.html')

@app.route('/predict')
def predict():
    if 'user' not in session:
        return redirect('/login')
    return render_template('predict.html')

@app.route('/result', methods=['POST'])
def result():
    if 'user' not in session:
        return redirect('/login')
    try:
        data = [
            float(request.form['income']),
            float(request.form['age']),
            float(request.form['rooms']),
            float(request.form['bedrooms']),
            float(request.form['population'])
        ]
        prediction = model.predict([data])[0]
        return render_template('result.html', prediction=round(prediction, 2))
    except:
        return "Error: Please enter valid numeric values."

@app.route('/data')
def data():
    df = pd.read_csv("USA_Housing.csv")
    return render_template('data.html', tables=[df.head(20).to_html(classes='table', header=True, index=False)])

@app.route('/visualize')
def visualize():
    return render_template('visualize.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

# ------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
