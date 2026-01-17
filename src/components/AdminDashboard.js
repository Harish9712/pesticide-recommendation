import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const AdminDashboard = ({ user, onLogout }) => {
  const [stats, setStats] = useState({
    totalPredictions: 0,
    healthyPlants: 0,
    diseasedPlants: 0,
    topDiseases: []
  });
  const [recentPredictions, setRecentPredictions] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Simulate loading admin data
    loadAdminData();
  }, []);

  const loadAdminData = async () => {
    try {
      // Simulate API call to get admin statistics
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock data - in real app, this would come from your backend
      setStats({
        totalPredictions: 128,
        healthyPlants: 89,
        diseasedPlants: 39,
        topDiseases: [
          { name: 'Tomato Early Blight', count:20 },
          { name: 'Apple Scab', count: 38 },
          { name: 'Corn Common Rust', count: 32 },
          { name: 'Potato Late Blight', count: 28 }
        ]
      });

      setRecentPredictions([
        { id: 1, image: 'plant1.jpg', disease: 'Tomato Early Blight', confidence: 0.92, timestamp: '2025-10-15 14:30' },
        { id: 2, image: 'plant2.jpg', disease: 'Healthy', confidence: 0.88, timestamp: '2025-10-15 14:25' },
        { id: 3, image: 'plant3.jpg', disease: 'Apple Scab', confidence: 0.95, timestamp: '2025-10-15 14:20' },
        { id: 4, image: 'plant4.jpg', disease: 'Corn Common Rust', confidence: 0.89, timestamp: '2025-10-15 14:15' }
      ]);
    } catch (error) {
      console.error('Failed to load admin data:', error);
    }
  };

  const handleLogout = () => {
    onLogout();
    navigate('/');
  };

  const handleGoToPredict = () => {
    navigate('/predict');
  };

  return (
    <div className="min-vh-100" style={{ background: 'linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%)' }}>
      {/* Header */}
      <nav className="navbar navbar-expand-lg navbar-dark" style={{ background: 'linear-gradient(135deg, #2d5a27 0%, #4a7c59 100%)' }}>
        <div className="container">
          <a className="navbar-brand" href="#">
            <i className="fas fa-seedling me-2"></i>
            Admin Dashboard
          </a>
          <div className="navbar-nav ms-auto">
            <span className="navbar-text me-3">
              <i className="fas fa-user-shield me-1"></i>
              {user.email}
            </span>
            <button className="btn btn-outline-light me-2" onClick={handleGoToPredict}>
              <i className="fas fa-search me-1"></i>Predict
            </button>
            <button className="btn btn-outline-light" onClick={handleLogout}>
              <i className="fas fa-sign-out-alt me-1"></i>Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="container py-4">
        {/* Welcome Section */}
        <div className="row mb-4">
          <div className="col-12">
            <div className="card border-0 shadow-sm">
              <div className="card-body">
                <h2 className="card-title text-success">
                  <i className="fas fa-tachometer-alt me-2"></i>
                  Welcome to Admin Dashboard
                </h2>
                <p className="card-text text-muted">
                  Monitor and manage the Plant Disease Classification system
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="row mb-4">
          <div className="col-md-3 mb-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body text-center">
                <i className="fas fa-chart-line fa-2x text-primary mb-3"></i>
                <h3 className="text-primary">{stats.totalPredictions.toLocaleString()}</h3>
                <p className="text-muted mb-0">Total Predictions</p>
              </div>
            </div>
          </div>
          <div className="col-md-3 mb-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body text-center">
                <i className="fas fa-leaf fa-2x text-success mb-3"></i>
                <h3 className="text-success">{stats.healthyPlants.toLocaleString()}</h3>
                <p className="text-muted mb-0">Healthy Plants</p>
              </div>
            </div>
          </div>
          <div className="col-md-3 mb-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body text-center">
                <i className="fas fa-exclamation-triangle fa-2x text-warning mb-3"></i>
                <h3 className="text-warning">{stats.diseasedPlants.toLocaleString()}</h3>
                <p className="text-muted mb-0">Diseased Plants</p>
              </div>
            </div>
          </div>
          <div className="col-md-3 mb-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body text-center">
                <i className="fas fa-percentage fa-2x text-info mb-3"></i>
                <h3 className="text-info">
                  {((stats.healthyPlants / stats.totalPredictions) * 100).toFixed(1)}%
                </h3>
                <p className="text-muted mb-0">Health Rate</p>
              </div>
            </div>
          </div>
        </div>

        <div className="row">
          {/* Top Diseases */}
          <div className="col-md-6 mb-4">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-header bg-success text-white">
                <h5 className="mb-0">
                  <i className="fas fa-chart-bar me-2"></i>
                  Top Diseases Detected
                </h5>
              </div>
              <div className="card-body">
                {stats.topDiseases.map((disease, index) => (
                  <div key={index} className="d-flex justify-content-between align-items-center mb-3">
                    <div>
                      <strong>{disease.name}</strong>
                      <br />
                      <small className="text-muted">{disease.count} cases</small>
                    </div>
                    <div className="text-end">
                      <span className="badge bg-primary">
                        #{index + 1}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Recent Predictions */}
          <div className="col-md-6 mb-4">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-header bg-info text-white">
                <h5 className="mb-0">
                  <i className="fas fa-clock me-2"></i>
                  Recent Predictions
                </h5>
              </div>
              <div className="card-body">
                {recentPredictions.map((prediction) => (
                  <div key={prediction.id} className="d-flex justify-content-between align-items-center mb-3">
                    <div>
                      <strong>{prediction.disease}</strong>
                      <br />
                      <small className="text-muted">{prediction.timestamp}</small>
                    </div>
                    <div className="text-end">
                      <span className={`badge ${prediction.disease === 'Healthy' ? 'bg-success' : 'bg-warning'}`}>
                        {(prediction.confidence * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="row">
          <div className="col-12">
            <div className="card border-0 shadow-sm">
              <div className="card-header bg-secondary text-white">
                <h5 className="mb-0">
                  <i className="fas fa-tools me-2"></i>
                  Quick Actions
                </h5>
              </div>
              <div className="card-body">
                <div className="row">
                  <div className="col-md-3 mb-2">
                    <button className="btn btn-outline-primary w-100" onClick={handleGoToPredict}>
                      <i className="fas fa-search me-2"></i>
                      New Prediction
                    </button>
                  </div>
                  <div className="col-md-3 mb-2">
                    <button className="btn btn-outline-success w-100">
                      <i className="fas fa-download me-2"></i>
                      Export Data
                    </button>
                  </div>
                  <div className="col-md-3 mb-2">
                    <button className="btn btn-outline-info w-100">
                      <i className="fas fa-chart-pie me-2"></i>
                      View Reports
                    </button>
                  </div>
                  <div className="col-md-3 mb-2">
                    <button className="btn btn-outline-warning w-100">
                      <i className="fas fa-cog me-2"></i>
                      Settings
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
