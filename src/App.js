import React, { useState, useCallback } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import AdminDashboard from './components/AdminDashboard';
import ProtectedRoute from './components/ProtectedRoute';
import PredictionPage from './components/PredictionPage';
import './App.css';

const PREDICTION_STORAGE_KEY = 'plant_disease_predictions';

function loadPredictionsFromStorage() {
  try {
    const stored = localStorage.getItem(PREDICTION_STORAGE_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
  } catch (e) {
    console.warn('Failed to load predictions from storage', e);
  }
  return [];
}

function savePredictionsToStorage(predictions) {
  try {
    localStorage.setItem(PREDICTION_STORAGE_KEY, JSON.stringify(predictions));
  } catch (e) {
    console.warn('Failed to save predictions to storage', e);
  }
}

function App() {
  const [user, setUser] = useState(null);
  const [predictionHistory, setPredictionHistory] = useState(loadPredictionsFromStorage);

  const addPrediction = useCallback((entry) => {
    const now = new Date();
    const dateStr = now.toLocaleDateString();
    const timeStr = now.toLocaleTimeString();
    const newEntry = {
      id: Date.now(),
      disease: entry.disease || 'No prediction',
      location: entry.location || 'Unknown',
      date: dateStr,
      time: timeStr,
      dateTime: `${dateStr} ${timeStr}`,
      confidence: entry.confidence ?? null,
    };
    setPredictionHistory((prev) => {
      const next = [newEntry, ...prev];
      savePredictionsToStorage(next);
      return next;
    });
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route 
            path="/" 
            element={
              user ? (
                <Navigate to={user.role === 'admin' ? '/admin' : '/predict'} replace />
              ) : (
                <Login onLogin={handleLogin} />
              )
            } 
          />
          <Route 
            path="/admin" 
            element={
              <ProtectedRoute user={user} requiredRole="admin">
                <AdminDashboard user={user} onLogout={handleLogout} predictionHistory={predictionHistory} />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/predict" 
            element={
              <ProtectedRoute user={user}>
                <PredictionPage user={user} onLogout={handleLogout} onPredictionRecord={addPrediction} />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
