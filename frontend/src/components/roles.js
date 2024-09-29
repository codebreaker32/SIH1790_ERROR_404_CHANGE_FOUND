import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/roles.css'; // Import the specific CSS file

function Roles() {
  const navigate = useNavigate();

  return (
    <div className="roles-container">
      <h1 className="main-heading">MISSING ITEM AND PERSON DETECTION</h1>
      <div className="login-options">
        <h2 className="sub-heading">LOGIN PAGE</h2>
        <button className="login-button" onClick={() => navigate('/admin-login')} style={{ marginBottom: '15px' }}>
          Staff Login
        </button>
        <button className="login-button" onClick={() => navigate('/branch-login')}>
          File Missing Report 
        </button>
      </div>
    </div>
  );
}

export default Roles;
