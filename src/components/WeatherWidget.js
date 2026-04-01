import React, { useState, useEffect } from 'react';

const PLACES = [
  { name: 'Coimbatore', lat: 11.0168, lon: 76.9558 },
  { name: 'Tirupur', lat: 11.1085, lon: 77.3411 },
  { name: 'Salem', lat: 11.6643, lon: 78.1460 },
  { name: 'Theni', lat: 10.0104, lon: 77.4768 },
];

const WeatherWidget = ({ selectedPlace: controlledPlace, onPlaceChange }) => {
  const [internalPlace, setInternalPlace] = useState('Coimbatore');
  const selectedPlace = controlledPlace ?? internalPlace;
  const setSelectedPlace = onPlaceChange ?? setInternalPlace;
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const place = PLACES.find((p) => p.name === selectedPlace);
    if (!place) return;

    setLoading(true);
    setError(null);

    const url = `https://api.open-meteo.com/v1/forecast?latitude=${place.lat}&longitude=${place.lon}&current=temperature_2m,relative_humidity_2m,weather_code&timezone=Asia/Kolkata`;

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        if (data.current) {
          setWeather(data.current);
        } else {
          setError('Could not fetch weather');
        }
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [selectedPlace]);

  return (
    <div className="header-info-card weather-widget-card">
      <div className="header-info-icon">
        <i className="fas fa-cloud-sun"></i>
      </div>
      <div className="header-info-content flex-grow-1">
        <h5 className="header-info-title">
          <i className="fas fa-map-marker-alt me-1"></i>Location & Weather
        </h5>
        <select
          className="form-select form-select-sm weather-select"
          value={selectedPlace}
          onChange={(e) => setSelectedPlace(e.target.value)}
        >
          <option value="Coimbatore">Coimbatore</option>
          <option value="Tirupur">Tirupur</option>
          <option value="Salem">Salem</option>
          <option value="Theni">Theni</option>
        </select>
        {loading && (
          <small className="weather-status">
            <i className="fas fa-spinner fa-spin me-1"></i>Loading...
          </small>
        )}
        {error && (
          <small className="weather-error">{error}</small>
        )}
        {weather && !loading && (
          <div className="weather-data">
            <span className="weather-temp">{weather.temperature_2m}°C</span>
            <span className="weather-humidity">{weather.relative_humidity_2m}% humidity</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default WeatherWidget;
