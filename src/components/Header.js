import React from 'react';
import WeatherWidget from './WeatherWidget';

const Header = ({ selectedPlace, onPlaceChange }) => {
  return (
    <div className="header-section">
      <div className="container">
        <div className="row align-items-center">
          <div className="col-lg-6 col-12 mb-3 mb-lg-0">
            <h1 className="header-title">
              <i className="fas fa-seedling me-2"></i>AI Plant Disease Classifier
            </h1>
            <p className="header-subtitle">
              Upload a plant leaf image to identify diseases and get pesticide recommendations
            </p>
          </div>
          <div className="col-lg-6 col-12">
            <div className="header-cards">
              <WeatherWidget selectedPlace={selectedPlace} onPlaceChange={onPlaceChange} />
              <div className="header-info-card">
                <div className="header-info-icon">
                  <i className="fas fa-brain"></i>
                </div>
                <div className="header-info-content">
                  <h5 className="header-info-title">AI-Powered</h5>
                  <p className="header-info-desc">Pesticide Recommendations using </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;
