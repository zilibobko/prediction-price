from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов
CORS(app, resources={r"/predict": {"origins": "http://localhost:3000"}})

# Загрузка модели и скейлеров
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler_x.pkl", "rb") as f:
    scaler_x = pickle.load(f)

with open("scaler_y.pkl", "rb") as f:
    scaler_y = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Получение данных из запроса
        data = request.get_json()
        print("[Лог бэкенда] Получены данные:", data)
        # Валидация входных данных
        required_fields = ['rooms', 'area', 'floor', 'total_floors', 'furniture', 'property_type']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        if not all(isinstance(data[field], (int, float)) for field in required_fields):
            return jsonify({'error': 'Invalid data types'}), 400

        # Подготовка данных для модели
        input_data = np.array([
            data['rooms'],
            data['area'],
            data['floor'],
            data['total_floors'],
            data['furniture'],
            data['property_type']
        ]).reshape(1, -1)
        
        # Масштабирование
        scaled_input = scaler_x.transform(input_data)
        
        # Предсказание
        scaled_prediction = model.predict(scaled_input)
        
        # Обратное масштабирование
        prediction = scaler_y.inverse_transform(scaled_prediction.reshape(-1, 1))
        print("Предсказание:", prediction)
        return jsonify({
            'predicted_price': round(float(prediction[0][0]), 2)
        })
        print("[Лог бэкенда] Предсказание:", prediction)
        return jsonify({'predicted_price': prediction})

    except Exception as e:
        print("[Лог бэкенда] Ошибка:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return jsonify({
        'message': 'Real Estate Price Prediction API',
        'status': 'active',
        'endpoints': ['POST /predict']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
