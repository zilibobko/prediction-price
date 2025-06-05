import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    rooms: 1,
    area: 30,
    floor: 1,
    total_floors: 5,
    furniture: 1,
    property_type: 0
  });
  const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const[error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: Number(value)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
      setLoading(true);
      setError(null);
    
      try {
        console.log("Отправляемые данные:", formData);
          const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
            body: JSON.stringify({
                rooms: Number(formData.rooms),
                area: Number(formData.area),
                floor: Number(formData.floor),
                total_floors: Number(formData.total_floors),
                furniture: Number(formData.furniture),
                property_type: Number(formData.property_type)
            }),
            mode: 'cors',
            credentials: 'include'
      });
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      const data = await response.json();
      if (data.status === 'error') {
              throw new Error(data.error);
      }
      setPrediction(data.predicted_price);
    } catch (error) {
          console.error('Error:', error);
          setError(error.message);
          alert("Ошибка при отправке запроса. Проверьте консоль для деталей.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Определение цены на недвижимость</h1>
        <form onSubmit={handleSubmit} className="prediction-form">
          <div className="form-group">
            <label>Количество комнат:</label>
            <input
              type="number"
              name="rooms"
              min="1"
              value={formData.rooms}
              onChange={handleChange}
            />
          </div>
          
          <div className="form-group">
            <label>Площадь (м²):</label>
            <input
              type="number"
              name="area"
              min="10"
              step="0.1"
              value={formData.area}
              onChange={handleChange}
            />
          </div>
          
          <div className="form-group">
            <label>Этаж:</label>
            <input
              type="number"
              name="floor"
              min="1"
              value={formData.floor}
              onChange={handleChange}
            />
          </div>
          
          <div className="form-group">
            <label>Всего этажей:</label>
            <input
              type="number"
              name="total_floors"
              min="1"
              value={formData.total_floors}
              onChange={handleChange}
            />
          </div>
          
          <div className="form-group">
            <label>Мебель:</label>
            <select
              name="furniture"
              value={formData.furniture}
              onChange={handleChange}
            >
              <option value="1">Есть</option>
              <option value="0">Нет</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Тип недвижимости:</label>
            <select
              name="property_type"
              value={formData.property_type}
              onChange={handleChange}
            >
              <option value="0">Вторичное жилье</option>
              <option value="1">Новостройка</option>
            </select>
          </div>
          
          <button type="submit" disabled={loading}>
            {loading ? 'Определяем...' : 'Определить цену'}
          </button>
        </form>
        
        {prediction !== null && (
          <div className="prediction-result">
            <h2>Цена определена:</h2>
            <p>{Math.round(prediction).toLocaleString()} руб.</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;