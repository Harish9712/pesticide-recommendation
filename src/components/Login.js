import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Check credentials
      if (email === 'harish.admin@hms.in' && password === 'Harish2004'|| email==='sangamithra.admin@hms.in' && password==='Madhu2005'|| email==='srinivasan.admin@hms.in' && password==='12345678') {
        onLogin({ email, role: 'admin' });
        navigate('/admin');
      } else if (email !== 'harish.admin@hms.in' && password !== 'Harish2004' && email !== 'sangamithra.admin@hms.in' && password !== 'Madhu2005' && email !== 'srinivasan.admin@hms.in' && password !== '12345678') {
        onLogin({ email, role: 'user' });
        navigate('/predict');
      } else {
        setError('Please enter both email and password');
      }
    } catch (err) {
      setError('Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page-wrapper min-vh-100 d-flex align-items-center justify-content-center" style={{ position: 'relative' }}>
      <div
        className="login-page-bg"
        style={{
          position: 'absolute',
          inset: 0,
          zIndex: -1,
          backgroundImage: "url('/farmer.png')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
        }}
      />
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-6 col-lg-4">
            <div className="card shadow-lg border-0" style={{ borderRadius: '15px', background: 'rgba(255, 255, 255, 0.7)', backdropFilter: 'blur(8px)' }}>
              <div className="card-body p-5" style={{ background: 'transparent' }}>
                <div className="text-center mb-4">
                  <i className="fas fa-seedling fa-3x text-success mb-3"></i>
                  <h3 className="fw-bold text-success">Plant Disease Classifier</h3>
                  <p className="text-muted">Sign in to continue</p>
                </div>

                <form onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email Address</label>
                    <div className="input-group">
                      <span className="input-group-text">
                        <i className="fas fa-envelope"></i>
                      </span>
                      <input
                        type="email"
                        className="form-control"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                        required
                      />
                    </div>
                  </div>

                  <div className="mb-4">
                    <label htmlFor="password" className="form-label">Password</label>
                    <div className="input-group">
                      <span className="input-group-text">
                        <i className="fas fa-lock"></i>
                      </span>
                      <input
                        type="password"
                        className="form-control"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                        required
                      />
                    </div>
                  </div>

                  {error && (
                    <div className="alert alert-danger" role="alert">
                      <i className="fas fa-exclamation-triangle me-2"></i>
                      {error}
                    </div>
                  )}

                  <button
                    type="submit"
                    className="btn btn-success w-100 py-2"
                    disabled={loading}
                    style={{ borderRadius: '25px' }}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        Signing in...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-sign-in-alt me-2"></i>
                        Sign In
                      </>
                    )}
                  </button>
                </form>

                {/* <div className="text-center mt-4">
                  <small className="text-muted">
                    <strong>Demo Credentials:</strong><br />
        
                    User: any email / any password
                  </small>
                </div> */}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
