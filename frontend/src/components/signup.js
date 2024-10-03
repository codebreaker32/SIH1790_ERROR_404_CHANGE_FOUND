import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // Import axios
import '../css/signup.css';

function Signup() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [error, setError] = useState(''); // State for error messages

  const handleSignup = async (e) => {
    e.preventDefault();

    // Basic validation
    if (!name || !phone || phone.length !== 10 || !password1 || password1 !== password2) {
      if (password1 !== password2) {
        alert('Passwords do not match');
      } else if (phone.length !== 10) {
        alert('Please enter a valid 10-digit phone number');
      }
      return; // Exit the function if validation fails
    }

    try {
      // Send signup data to the backend
      const response = await axios.post('https://simhastha-backend.livelyisland-13266f7c.centralindia.azurecontainerapps.io/staff/signup/', {
        name,
        phone,
        password: password1,
      });

      // Handle successful signup
      if (response.status === 201) { // Assuming 201 status is returned on success
        alert('Signup successful! Redirecting to login page...');
        navigate('/admin-login');
      }
    } catch (err) {
      // Handle error responses from the server
      if (err.response) {
        // The request was made and the server responded with a status code
        setError(err.response.data.message || 'An error occurred during signup.'); // Adjust according to your backend response
      } else {
        setError('Network error, please try again later.');
      }
    }
  };

  return (
    <div className="signup-container">
      <h1>Sign Up</h1>
      {error && <p className="error-message">{error}</p>} {/* Display error message */}
      <form onSubmit={handleSignup}>
        <div className="form-group">
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your name"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="phone">Phone Number</label>
          <input
            type="tel"
            id="phone"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="Enter your phone number"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password1">Password</label>
          <input
            type="password"
            id="password1"
            value={password1}
            onChange={(e) => setPassword1(e.target.value)}
            placeholder="Enter password"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password2">Confirm Password</label>
          <input
            type="password"
            id="password2"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
            placeholder="Confirm password"
            required
          />
        </div>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default Signup;

