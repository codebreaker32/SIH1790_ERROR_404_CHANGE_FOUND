import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/branchlogin.css';

function BranchLogin() {
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [generatedOtp, setGeneratedOtp] = useState(''); // You can keep this for testing if needed
  const [isOtpSent, setIsOtpSent] = useState(false);
  const [isOtpVerified, setIsOtpVerified] = useState(false);
  const navigate = useNavigate();

  // Function to simulate sending OTP via an AJAX request
  const sendOtp = (e) => {
    e.preventDefault();

    // Simulate OTP generation (e.g., backend sends OTP to the user's phone number)
    const simulatedOtp = Math.floor(1000 + Math.random() * 9000).toString(); // Random 4-digit OTP
    setGeneratedOtp(simulatedOtp);
    setIsOtpSent(true);

    // Log OTP to console instead of alert
    console.log('Sending OTP to:', phone, 'OTP:', simulatedOtp);
    // Remove the alert for displaying OTP
    // alert(`OTP sent to your phone: ${simulatedOtp}`);
  };

  // Function to verify OTP
  const verifyOtp = (e) => {
    e.preventDefault();
    // Allow any OTP input to succeed
    setIsOtpVerified(true);
    console.log('OTP verified successfully');
    navigate('/user-dashboard'); // Navigate to the User Dashboard upon success
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

