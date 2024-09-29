import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/adminlogin.css'; 

function AdminLogin() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    if (username && password) {
      // Redirect to the Staff Dashboard instead of Admin Dashboard
      navigate('/staff-dashboard');
    }
  };

  return (
    <div className="admin-login-container">
      <div className="login-card">
        <h1 className="title">Staff Login</h1>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </div>
          <button type="submit" className="login-button">Login</button>
        </form>
        <div className="link">
          <p>Don't have an account? <a href="/signup">Sign Up</a></p>
        </div>
      </div>
    </div>
  );
}

export default AdminLogin;


