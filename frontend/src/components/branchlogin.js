import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../css/branchlogin.css';

function BranchLogin() {
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [isOtpSent, setIsOtpSent] = useState(false);
  const [isOtpVerified, setIsOtpVerified] = useState(false);
  const navigate = useNavigate();

  // Function to send OTP to the user's phone
  const sendOtp = async (e) => {
    e.preventDefault();

    try {
      // Make a POST request to send OTP
      const response = await axios.post('https://simhastha-backend.livelyisland-13266f7c.centralindia.azurecontainerapps.io/send-otp/', {
        phone, // Send the phone number
      });

      if (response.status === 200) {
        setIsOtpSent(true);
        alert(`OTP sent to your phone: ${response.data.otp}`); // Assuming your backend sends the OTP in the response
      } else {
        alert('Failed to send OTP. Please try again.');
      }
    } catch (error) {
      console.error('Error sending OTP:', error);
      alert('Error sending OTP. Please try again later.');
    }
  };

  // Function to verify OTP
  const verifyOtp = async (e) => {
    e.preventDefault();

    try {
      // Make a POST request to verify the OTP
      const response = await axios.post('https://simhastha-backend.livelyisland-13266f7c.centralindia.azurecontainerapps.io/verify-otp/', {
        phone,
        otp, // Send the OTP entered by the user
      });

      if (response.status === 200) {
        setIsOtpVerified(true);
        console.log('OTP verified successfully');
        navigate('/user-dashboard'); // Navigate to the User Dashboard upon success
      } else {
        alert('Invalid OTP, please try again.');
      }
    } catch (error) {
      console.error('Error verifying OTP:', error);
      alert('Invalid OTP, please try again.');
    }
  };

  return (
    <div className="branch-login-container">
      <div className="login-card">
        <h2>User Login</h2>
        {!isOtpSent ? (
          <form onSubmit={sendOtp}>
            <div className="input-group">
              <label htmlFor="phone">Phone Number:</label>
              <input
                type="tel"
                id="phone"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="login-button">Send OTP</button>
          </form>
        ) : (
          <form onSubmit={verifyOtp}>
            <div className="input-group">
              <label htmlFor="otp">Enter OTP:</label>
              <input
                type="text"
                id="otp"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="login-button">Verify OTP</button>
          </form>
        )}
        {isOtpVerified && <p>Login successful!</p>}
      </div>
    </div>
  );
}

export default BranchLogin;

