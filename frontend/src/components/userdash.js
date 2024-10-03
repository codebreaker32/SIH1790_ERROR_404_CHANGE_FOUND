import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // Import axios
import '../css/userdash.css';

Modal.setAppElement('#root');

const UserDashboard = () => {
  const [image, setImage] = useState(null);
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [gender, setGender] = useState('');
  const [reportType, setReportType] = useState('');
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState('');
  const [isImageRequired, setIsImageRequired] = useState(false);
  const [isGenderFieldVisible, setIsGenderFieldVisible] = useState(false);
  const [isReportModalOpen, setIsReportModalOpen] = useState(false);
  const [reports, setReports] = useState([]);
  const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false);
  const navigate = useNavigate();
let personCounter = 1;
  let objectCounter = 1;
  // Fetch existing reports from the backend
  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await axios.get('/api/reports'); // Adjust the endpoint as needed
        setReports(response.data);
      } catch (error) {
        console.error('Error fetching reports:', error);
      }
    };

    fetchReports();
  }, []);

  const handleFileReport = async (e) => {
    e.preventDefault();

    if (reportType === 'missing_person' && !image) {
      alert('Image is required for missing person reports.');
      return;
    }

    const formData = new FormData();
    formData.append('name', name);
    formData.append('age', age);
    formData.append('phoneNumber', phoneNumber);
    formData.append('gender', isGenderFieldVisible ? gender : '');
    formData.append('image', image);
    formData.append('reportType', reportType);
    formData.append('description', description);
    formData.append('location', location);
    formData.append('status', 'Pending');
     try {
      // Assign report ID based on report type
      let reportId;
      if (reportType === 'missing_person') {
        reportId = `PERSON_${personCounter++}`;
      } else if (reportType === 'missing_item') {
        reportId = `OBJECT_${objectCounter++}`;
      }

      // Add reportId to the formData
      formData.append('id', reportId);
      // Send POST request to save the report
      const response = await axios.post('/api/reports', formData); // Adjust the endpoint as needed
      setReports([...reports, response.data]); // Add the newly created report to the local state
      setIsReportModalOpen(true);
    } catch (error) {
      console.error('Error submitting report:', error);
      alert('There was an error submitting your report. Please try again.');
    }

    // Clear the form fields
    setName('');
    setAge('');
    setPhoneNumber('');
    setGender('');
    setImage(null);
    setReportType('');
    setDescription('');
    setLocation('');
  };

  const handleReportTypeChange = (e) => {
    const selectedType = e.target.value;
    setReportType(selectedType);
    setIsImageRequired(selectedType === 'missing_person');
    setIsGenderFieldVisible(selectedType === 'missing_person');
  };

  const openLogoutModal = () => setIsLogoutModalOpen(true);
  const closeLogoutModal = () => setIsLogoutModalOpen(false);
  const handleLogout = () => {
    alert('Logged out successfully!');
    closeLogoutModal();
    navigate('/');
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setReports((prevReports) =>
        prevReports.filter((report) => report.status !== 'Closed')
      );
    }, 5000);

    return () => clearInterval(interval);
  }, [reports]);

  return (
    <div className="user-dashboard">
      <h1>USER DASHBOARD</h1>

      {/* File a Missing Report Section */}
      <div className="file-report-section">
        <h2>File Missing Report</h2>
        <form onSubmit={handleFileReport}>
          {/* Input fields remain the same */}
          <div className="input-group">
            <label htmlFor="name">Name of person or object:</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter name"
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="age">Age of person or item:</label>
            <input
              type="number"
              id="age"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              placeholder="Enter age"
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="phoneNumber">Phone Number:</label>
            <input
              type="tel"
              id="phoneNumber"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              placeholder="Enter phone number"
              required
            />
          </div>
          {isGenderFieldVisible && (
            <div className="input-group">
              <label htmlFor="gender">Gender:</label>
              <select
                id="gender"
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                required
              >
                <option value="">Select Gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>
          )}
          <div className="input-group">
            <label htmlFor="image">Upload Image (Mandatory for missing person):</label>
            <input
              type="file"
              id="image"
              onChange={(e) => setImage(e.target.files[0])}
              required={isImageRequired}
            />
          </div>
          <div className="input-group">
            <label htmlFor="reportType">Report Type:</label>
            <select
              id="reportType"
              value={reportType}
              onChange={handleReportTypeChange}
              required
            >
              <option value="">Select Report Type</option>
              <option value="missing_person">Missing Person</option>
              <option value="missing_item">Missing Item</option>
            </select>
          </div>
          <div className="input-group">
            <label htmlFor="description">Description:</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="What they were wearing, last seen time, etc."
              required
            ></textarea>
          </div>
          <div className="input-group">
            <label htmlFor="location">Last Seen Location:</label>
            <input
              type="text"
              id="location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="Location where last seen"
              required
            />
          </div>
          <button type="submit" className="submit-report-button">
            Submit Report
          </button>
        </form>
      </div>

      {/* View All Filed Reports Section */}
      <div className="view-reports-section">
        <h2>View Filed Reports</h2>
        <ul className="report-list">
          {reports.length === 0 ? (
            <li>No reports filed yet.</li>
          ) : (
            reports.map((report) => (
              <li key={report.id} className="report-item">
                <strong>Report ID:</strong> {report.id}<br />
                <strong>Name:</strong> {report.name}<br />
                <strong>Age:</strong> {report.age} years<br />
                <strong>Phone Number:</strong> {report.phoneNumber}<br />
                <strong>Gender:</strong> {report.gender || 'N/A'}<br />
                <strong>Report Type:</strong>{' '}
                {report.reportType === 'missing_person'
                  ? 'Missing Person'
                  : 'Missing Item'}<br />
                <strong>Status:</strong> {report.status || 'Pending'}
		     {report.image && (
                  <>
                    <strong>Image:</strong><br />
                    <img
                      src={URL.createObjectURL(report.image)}
                      alt={report.name}
                      style={{ width: '150px', height: '150px', objectFit: 'cover' }}
                    />
                  </>
                )}
              </li>
            ))
          )}
        </ul>
      </div>

      {/* Logout Button Section */}
      <div className="logout-section">
        <button className="logout-btn" onClick={openLogoutModal}>Logout</button>
        <Modal
          isOpen={isLogoutModalOpen}
          onRequestClose={closeLogoutModal}
          contentLabel="Logout Confirmation"
          className="modal-content"
          overlayClassName="modal-overlay"
        >
          <h2>Logout Confirmation</h2>
          <p>Are you sure you want to logout?</p>
          <button onClick={handleLogout}>Yes</button>
          <button onClick={closeLogoutModal}>No</button>
        </Modal>
      </div>

      {/* Confirmation Modal for report submission */}
      <Modal
        isOpen={isReportModalOpen}
        onRequestClose={() => setIsReportModalOpen(false)}
        contentLabel="Report Submitted"
        className="modal-content"
        overlayClassName="modal-overlay"
      >
        <h2>Report Submitted Successfully!</h2>
        <p>Your report has been filed.</p>
        <button onClick={() => setIsReportModalOpen(false)}>Close</button>
      </Modal>
    </div>
  );
};

export default UserDashboard;

