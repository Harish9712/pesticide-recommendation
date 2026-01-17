import React from 'react';

const Header = () => {
  return (
    <div className="header-section">
      <div className="container">
        <div className="row align-items-center">
          <div className="col-md-8">
            <h1 className="mb-2">
              <i className="fas fa-seedling me-3"></i>AI Plant Disease Classifier
            </h1>
            <p className="lead mb-0">
              Upload a plant leaf image to identify diseases and get pesticide recommendations
            </p>
          </div>
          <div className="col-md-4 text-end">
            <div className="stats-card">
              <i className="fas fa-brain feature-icon"></i>
              <h5 className="mb-1">AI-Powered</h5>
              <small className="text-muted">Advanced ML Model</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;
