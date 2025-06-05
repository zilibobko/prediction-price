from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/predict": {
    "origins": ["https://stalwart-lolly-8a721c.netlify.app", 
                "http://localhost:3000"],
    "methods": ["POST", "OPTIONS"],
    "allow_headers": ["Content-Type"], "supports_credentials": True}}
     )


with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler_x.pkl", "rb") as f:
    scaler_x = pickle.load(f)

with open("scaler_y.pkl", "rb") as f:
    scaler_y = pickle.load(f)

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    else:
      try:
        data = request.get_json()
        input_data = np.array([
            data['rooms'],
            data['area'],
            data['floor'],
            data['total_floors'],
            data['furniture'],
            data['property_type']
        ]).reshape(1, -1)
        
        scaled_input = scaler_x.transform(input_data)
        scaled_prediction = model.predict(scaled_input)
        prediction = scaler_y.inverse_transform(scaled_prediction.reshape(-1, 1))
        return jsonify({
            'predicted_price': round(float(prediction[0][0]), 2)
        })

      except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }),
@app.after_request
def add_cors_headers(response):
    response = jsonify({'message': 'Preflight'})
    response.headers.add('Access-Control-Allow-Origin', 'https://stalwart-lolly-8a721c.netlify.app/')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    return response
@app.route('/')
def home():
    return jsonify({
        'message': 'Real Estate Price Prediction API',
        'status': 'active',
        'endpoints': ['POST /predict']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
