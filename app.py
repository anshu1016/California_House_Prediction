import pickle
import numpy as np
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Load scaler and model
scalar = pickle.load(open('scaling.pkl', 'rb'))
regmodel = pickle.load(open('regressionModel.pkl', 'rb'))

# Home route
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Predict from form
@app.route('/predict', methods=['POST'])
def predict():
    try:
        form_data = request.form.to_dict()
        features = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']
        data = [float(form_data[feature]) for feature in features]
        final_input = scalar.transform(np.array(data).reshape(1, -1))
        output = regmodel.predict(final_input)[0]
        return render_template('index.html', prediction_text=f'The house price prediction is ${output:.2f}')
    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

# Predict from API
@app.route('/predict_api', methods=['POST'])
def predict_api():
    if request.json is None or 'data' not in request.json:
        return jsonify({'error': 'Invalid input. Expecting JSON with a "data" key.'}), 400

    try:
        data = request.json['data']
        input_array = np.array(list(data.values())).reshape(1, -1)
        transformed = scalar.transform(input_array)
        output = regmodel.predict(transformed)[0]
        return jsonify({'prediction': float(output)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
