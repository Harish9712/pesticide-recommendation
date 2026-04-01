import React, { useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import * as XLSX from 'xlsx';

const formatDiseaseName = (name) => {
  if (!name) return 'Unknown';
  return name.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());
};

const AdminDashboard = ({ user, onLogout, predictionHistory = [] }) => {
  const navigate = useNavigate();

  const { stats, topDiseases } = useMemo(() => {
    const total = predictionHistory.length;
    const diseaseCountMap = {};
    let healthy = 0;
    let diseased = 0;

    predictionHistory.forEach((p) => {
      const name = p.disease || 'Unknown';
      diseaseCountMap[name] = (diseaseCountMap[name] || 0) + 1;
      const lower = name.toLowerCase();
      if (lower.includes('healthy')) {
        healthy++;
      } else {
        diseased++;
      }
    });

    const top = Object.entries(diseaseCountMap)
      .map(([name, count]) => ({ name: formatDiseaseName(name), count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 8);

    return {
      stats: {
        totalPredictions: total,
        healthyPlants: healthy,
        diseasedPlants: diseased,
      },
      topDiseases: top,
    };
  }, [predictionHistory]);

  const handleLogout = () => {
    onLogout();
    navigate('/');
  };

  const handleGoToPredict = () => {
    navigate('/predict');
  };

  const handleExportData = () => {
    if (predictionHistory.length === 0) {
      alert('No data to export.');
      return;
    }
    const rows = predictionHistory.map((p) => ({
      Disease: formatDiseaseName(p.disease),
      Location: p.location,
      Date: p.date,
      Time: p.time,
      Confidence: p.confidence != null ? `${(p.confidence * 100).toFixed(1)}%` : '—',
    }));
    const ws = XLSX.utils.json_to_sheet(rows);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Predictions');
    const fileName = `plant_disease_predictions_${new Date().toISOString().slice(0, 10)}.xlsx`;
    XLSX.writeFile(wb, fileName);
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
                  {stats.totalPredictions > 0
                    ? ((stats.healthyPlants / stats.totalPredictions) * 100).toFixed(1)
                    : 0}%
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
                {topDiseases.length === 0 ? (
                  <p className="text-muted mb-0">No predictions yet. Predictions will appear here.</p>
                ) : (
                topDiseases.map((disease, index) => (
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
                ))
                )}
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
                {predictionHistory.length === 0 ? (
                  <p className="text-muted mb-0">No predictions yet.</p>
                ) : (
                  predictionHistory.slice(0, 15).map((p) => (
                    <div key={p.id} className="admin-prediction-row">
                      <div>
                        <strong>{formatDiseaseName(p.disease)}</strong>
                        <br />
                        <small className="text-muted">
                          <i className="fas fa-map-marker-alt me-1"></i>{p.location}
                          {' · '}
                          {p.date} {p.time}
                        </small>
                      </div>
                      <div className="text-end">
                        {p.confidence != null ? (
                          <span className={`badge ${p.disease?.toLowerCase().includes('healthy') ? 'bg-success' : 'bg-warning'}`}>
                            {(p.confidence * 100).toFixed(0)}%
                          </span>
                        ) : (
                          <span className="badge bg-secondary">—</span>
                        )}
                      </div>
                    </div>
                  ))
                )}
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
                    <button className="btn btn-outline-success w-100" onClick={handleExportData} disabled={predictionHistory.length === 0}>
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
