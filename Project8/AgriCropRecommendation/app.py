from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load model
with open('model/crop_model.pkl', 'rb') as f:
    model, le = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = [
            float(request.form['N']),
            float(request.form['P']),
            float(request.form['K']),
            float(request.form['temperature']),
            float(request.form['humidity']),
            float(request.form['ph']),
            float(request.form['rainfall']),
        ]
        result = model.predict([data])
        crop = le.inverse_transform(result)[0]
        return render_template('index.html', prediction=crop)
    except:
        return render_template('index.html', prediction="Invalid input!")

if __name__ == '__main__':
    app.run(debug=True)
