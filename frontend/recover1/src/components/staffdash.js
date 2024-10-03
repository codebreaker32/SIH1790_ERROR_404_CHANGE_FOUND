import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Modal from 'react-modal';
import { useNavigate } from 'react-router-dom';
import '../css/staffdash.css';

Modal.setAppElement('#root');

const StaffDashboard = () => {
  const [missingReports, setMissingReports] = useState([]);
  const [cameraFeed, setCameraFeed] = useState(null);
  const [faceRecognitionResult, setFaceRecognitionResult] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isHowToUseModalOpen, setIsHowToUseModalOpen] = useState(false);
  const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false);
  const [isCameraModalOpen, setIsCameraModalOpen] = useState(false);
  const [cameraError, setCameraError] = useState(null);
  const [isChatbotVisible, setIsChatbotVisible] = useState(false);

  const videoRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch missing reports from the backend
    const fetchMissingReports = async () => {
      try {
        const response = await axios.get('/api/missing-reports');
        let reports = Array.isArray(response.data) ? response.data : [];

        // Adding predefined reports
        const predefinedReports = [
          {
            id: "PERSON_1",
            name: "Harshdip Saha",
            age: 19,
            gender: "male",
            phoneNumber: "9228182636",
            reportType: "missing person",
            description: "Wearing a red coloured t-shirt with brown cargo",
            location: "near stall no. 48",
            status: "PENDING",
            photo: "harshdip.jpg" // Replace with actual URL
          },
          {
            id: "PERSON_2",
            name: "Anshuman Raj",
            age: 19,
            gender: "male",
            phoneNumber: "9588584453",
            reportType: "missing person",
            description: "Wearing blue white shirt with black jeans",
            location: "near MAIN gate entrance",
            status: "PENDING",
            photo: "thiss.jpeg" // Replace with actual URL
          }
        ];

        // Set the missing reports including predefined ones
        setMissingReports([...reports, ...predefinedReports]);
      } catch (error) {
        console.error('Error fetching reports:', error);
        setMissingReports([
          {
            id: "PERSON_1",
            name: "Harshdip Saha",
            age: 19,
            gender: "male",
            phoneNumber: "9228182636",
            reportType: "missing person",
            description: "Wearing a red coloured t-shirt with brown cargo",
            location: "near stall no. 48",
            status: "PENDING",
            photo: "harshdip.jpg" // Replace with actual URL
          },
          {
            id: "PERSON_2",
            name: "Anshuman Raj",
            age: 19,
            gender: "male",
            phoneNumber: "9588584453",
            reportType: "missing person",
            description: "Wearing blue white shirt with black jeans",
            location: "near MAIN gate entrance",
            status: "PENDING",
            photo: "thiss.jpeg" // Replace with actual URL
          }
        ]);
      }
    };

    fetchMissingReports();
  }, []);

  const handleAnalyzeCamera = async () => {
    try {
      const response = await axios.post('/api/analyze-camera', { cameraFeed });
      const { matchFound, confidence, personData } = response.data;

      if (matchFound && confidence > 0.85) {
        setFaceRecognitionResult({
          status: 'match',
          confidence,
          personData
        });
      } else {
        setFaceRecognitionResult({
          status: 'no-match',
          message: 'No match found, continuing tracking...'
        });
      }
    } catch (error) {
      console.error('Error analyzing camera feed:', error);
    }
  };

  const handleVerifyMatch = (personData) => {
    alert(`Match verified! Police notified for person: ${personData.name}`);
  };

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  const openHowToUseModal = () => {
    setIsHowToUseModalOpen(true);
    setIsChatbotVisible(true); // Show chatbot
  };

  const closeHowToUseModal = () => {
    setIsHowToUseModalOpen(false);
    setIsChatbotVisible(false); // Hide chatbot
  };

  const openLogoutModal = () => setIsLogoutModalOpen(true);
  const closeLogoutModal = () => setIsLogoutModalOpen(false);

  const openCameraModal = () => {
    setIsCameraModalOpen(true);
    requestCameraAccess();
  };

  const closeCameraModal = () => {
    setIsCameraModalOpen(false);
    if (videoRef.current) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach(track => track.stop());
    }
  };

  const requestCameraAccess = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      setCameraError(null);
      videoRef.current.srcObject = stream;
      videoRef.current.play();
    } catch (error) {
      setCameraError('Failed to access the camera. Please allow camera access.');
    }
  };

  const handleLogout = () => {
    setIsChatbotVisible(false); // Hide chatbot on logout
    navigate('/');
  };

  return (
    <div className="staff-dashboard">
      <h2 className="dashboard-title">Staff Dashboard</h2>

      {/* Missing Reports Section */}
      <div className="missing-reports-section">
        <h3 className="section-title">Missing Persons Reports</h3>
        <button className="view-reports-btn" onClick={openModal}>View Missing Reports</button>
        <Modal
          isOpen={isModalOpen}
          onRequestClose={closeModal}
          contentLabel="Missing Reports"
          className="modal-content"
          overlayClassName="modal-overlay"
        >
          <h2>All Missing Reports</h2>
          <div className="reports-container">
            {missingReports.map(report => (
              <div className="report-card" key={report.id}>
                <p><strong>Report ID:</strong> {report.id}</p>
                <p><strong>Name:</strong> {report.name}</p>
                <p><strong>Age:</strong> {report.age} years old</p>
                <p><strong>Gender:</strong> {report.gender}</p> {/* Display Gender */}
                <p><strong>Phone Number:</strong> {report.phoneNumber}</p>
                <p><strong>Report Type:</strong> {report.reportType}</p>
                <p><strong>Description:</strong> {report.description}</p>
                <p><strong>Last Seen:</strong> {report.location}</p>
                <p><strong>Status:</strong> {report.status}</p>
                {report.photo && <img src={report.photo} alt={report.name} className="report-photo" />} {/* Display Photo */}
              </div>
            ))}
          </div>
          <button className="close-modal-btn" onClick={closeModal}>Close</button>
        </Modal>
      </div>

      {/* Face Recognition Section */}
      <div className="camera-section">
        <h3 className="section-title">Analyze Camera Feed</h3>
        <button className="analyze-btn" onClick={openCameraModal}>View Camera Feed</button>
        <Modal
          isOpen={isCameraModalOpen}
          onRequestClose={closeCameraModal}
          contentLabel="Camera Feed"
          className="modal-content"
          overlayClassName="modal-overlay"
        >
          <h2>Camera Feed</h2>
          {cameraError ? (
            <p>{cameraError}</p>
          ) : (
            <video ref={videoRef} className="camera-feed" />
          )}
          <button className="close-modal-btn" onClick={closeCameraModal}>Close</button>
        </Modal>
      </div>

      {/* How to Use Section */}
      <div className="how-to-use-section">
        <button className="how-to-use-btn" onClick={openHowToUseModal}>How to Use</button>
        <Modal
          isOpen={isHowToUseModalOpen}
          onRequestClose={closeHowToUseModal}
          contentLabel="How to Use"
          className="modal-content"
          overlayClassName="modal-overlay"
        >
          <h2>How to Use the System</h2>
          <p>Follow the instructions to utilize the features effectively.</p>
	  <p><a href ="https://youtu.be/ocWosSs4PYA">YOUTUBE VIDEO FOR FURTHER INSTRUCTIONS</a></p>
	   <ul className="instructions-list">
            <li>View the missing persons reports by clicking "View Missing Reports".</li>
            <li>Analyze the camera feed for potential matches by clicking "View Camera Feed".</li>
            <li>If a match is found, verify the match and notify the police.</li>
            <li>You can always access this help section by clicking "How to Use".</li>
          </ul>
          <button className="close-modal-btn" onClick={closeHowToUseModal}>Close</button>
        </Modal>
      </div>

      {/* Logout Section */}
      <div className="logout-section">
        <button className="logout-btn" onClick={openLogoutModal}>Logout</button>
        <Modal
          isOpen={isLogoutModalOpen}
          onRequestClose={closeLogoutModal}
          contentLabel="Logout Confirmation"
          className="modal-content"
          overlayClassName="modal-overlay"
        >
          <h2>Are you sure you want to logout?</h2>
          <button className="confirm-logout-btn" onClick={handleLogout}>Yes, Logout</button>
          <button className="close-modal-btn" onClick={closeLogoutModal}>Cancel</button>
        </Modal>
      </div>
    </div>
  );
};

export default StaffDashboard;

