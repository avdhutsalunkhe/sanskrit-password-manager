from flask import Flask, render_template, request
import pickle
import numpy as np
import sqlite3

app = Flask(__name__)
model = pickle.load(open('model/crop_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        data = [float(x) for x in request.form.values()]
        final = np.array([data])
        result = model.predict(final)[0]

        # Save to DB
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO predictions (n, p, k, temp, humidity, ph, rainfall, crop) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (*data, result))
        conn.commit()
        conn.close()

        return render_template('predict.html', crop=result)
    return render_template('predict.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
