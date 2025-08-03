from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# === Load the model and label encoder safely ===
model_path = './model/crop_model.pkl'

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

with open(model_path, 'rb') as f:
    try:
        data = pickle.load(f)
    except Exception as e:
        raise ValueError(f"Error loading model file: {e}")

if isinstance(data, dict):
    model = data.get('model')
    le = data.get('le')
elif isinstance(data, (list, tuple)) and len(data) >= 2:
    model = data[0]
    le = data[1]
else:
    raise ValueError("Invalid format in model/crop_model.pkl. Expected dict or tuple.")

# === Flask Routes ===
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    crop = None
    error = None
    if request.method == 'POST':
        try:
            # Extract and validate form data
            features = []
            for key in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']:
                value = request.form.get(key)
                if value is None or value.strip() == '':
                    raise ValueError(f"Missing value for {key}")
                features.append(float(value))
            # Predict crop
            prediction = model.predict([features])[0]
            crop = le.inverse_transform([prediction])[0]
        except Exception as e:
            error = f"Prediction error: {e}"
    return render_template('recommendation.html', crop=crop, error=error)

# === Run App ===
if __name__ == '__main__':
    app.run(debug=True)
