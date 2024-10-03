import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // Import Axios
import '../css/adminlogin.css';

function AdminLogin() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(''); // State for error messages

  const handleLogin = async (e) => {
    e.preventDefault();

    if (username && password) {
      try {
        // Send login data to the backend
        const response = await axios.post('https://simhastha-backend.livelyisland-13266f7c.centralindia.azurecontainerapps.io/staff/login/', {
          username,
          password,
        });

        // Check the response status
        if (response.status === 200) {
          // Assuming 200 status is returned on successful login
          alert('Login successful! Redirecting to the dashboard...');
          navigate('/staff-dashboard');
        }
      } catch (err) {
        // Handle error responses from the server
        if (err.response) {
          setError(err.response.data.message || 'An error occurred during login.'); // Adjust according to your backend response
        } else {
          setError('Network error, please try again later.');
        }
      }
    }
  };

  return (
    <div className="admin-login-container">
      <div className="login-card">
        <h1 className="title">Staff Login</h1>
        {error && <p className="error-message">{error}</p>} {/* Display error message */}
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

