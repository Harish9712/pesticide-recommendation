import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from './Header';
import UploadSection from './UploadSection';
import ResultsSection from './ResultsSection';

const PredictionPage = ({ user, onLogout }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setResults(null);
    setError(null);
    
    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setImagePreview(e.target.result);
    };
    reader.readAsDataURL(file);
  };

  const handlePredict = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Request failed');
      }

      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
    setImagePreview(null);
    setResults(null);
    setError(null);
  };

  const handleLogout = () => {
    onLogout();
    navigate('/');
  };

  const handleGoToAdmin = () => {
    navigate('/admin');
  };

  return (
    <div className="App">
      {/* Navigation Bar */}
      <nav className="navbar navbar-expand-lg navbar-dark" style={{ background: 'linear-gradient(135deg, #2d5a27 0%, #4a7c59 100%)' }}>
        <div className="container">
          <a className="navbar-brand" href="#">
            <i className="fas fa-seedling me-2"></i>
            Plant Disease Classifier
          </a>
          <div className="navbar-nav ms-auto">
            <span className="navbar-text me-3">
              <i className="fas fa-user me-1"></i>
              {user.email}
            </span>
            {user.role === 'admin' && (
              <button className="btn btn-outline-light me-2" onClick={handleGoToAdmin}>
                <i className="fas fa-tachometer-alt me-1"></i>Admin
              </button>
            )}
            <button className="btn btn-outline-light" onClick={handleLogout}>
              <i className="fas fa-sign-out-alt me-1"></i>Logout
            </button>
          </div>
        </div>
      </nav>

      <Header />
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-lg-8">
            <UploadSection
              onFileSelect={handleFileSelect}
              onPredict={handlePredict}
              onReset={resetForm}
              selectedFile={selectedFile}
              imagePreview={imagePreview}
              loading={loading}
            />
            
            {error && (
              <div className="alert alert-danger mt-3">
                <i className="fas fa-exclamation-triangle me-2"></i>
                <strong>Error:</strong> {error}
              </div>
            )}

            {loading && (
              <div className="card result-card p-4 mt-3">
                <div className="text-center">
                  <div className="loading-spinner me-2"></div>
                  <h5>Analyzing your plant image...</h5>
                  <p className="text-muted">Please wait while our AI processes the image</p>
                </div>
              </div>
            )}

            {results && <ResultsSection results={results} />}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictionPage;
