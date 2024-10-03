import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import AdminLogin from './components/adminlogin';
import Signup from './components/signup';
import Roles from './components/roles';
import BranchLogin from './components/branchlogin';
import StaffDashboard from './components/staffdash';
import UserDashboard from './components/userdash';

function App() {

  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Roles />} />
          <Route path="/admin-login" element={<AdminLogin />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/branch-login" element={<BranchLogin />} />
          <Route path="/staff-dashboard" element={<StaffDashboard />} />
          <Route path="/user-dashboard" element={<UserDashboard />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;

