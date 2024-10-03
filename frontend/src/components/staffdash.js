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
        const response = await axios.get('/api/missing-reports', {
          // Add headers or token for authentication if required
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        // Check if the response data is an array
        if (Array.isArray(response.data)) {
          setMissingReports(response.data);
        } else {
          console.error('Unexpected response format:', response.data);
          setMissingReports([]); // Set to empty array if not valid
        }
      } catch (error) {
        console.error('Error fetching reports:', error);
        setMissingReports([]); // Set to empty array on error
      }
    };

    fetchMissingReports();
  }, []);

  const handleAnalyzeCamera = async () => {
    try {
      // Simulate camera feed analysis using a face recognition API
      const response = await axios.post('/api/analyze-camera', { cameraFeed }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      const { matchFound, confidence, personData } = response.data;

      if (matchFound && confidence > 0.85) {
        setFaceRecognitionResult({
          status: 'match',
          confidence,
          personData,
        });
        handleVerifyMatch(personData); // Notify police for a verified match
      } else {
        setFaceRecognitionResult({
          status: 'no-match',
          message: 'No match found, continuing tracking...',
        });
      }
    } catch (error) {
      console.error('Error analyzing camera feed:', error);
      setCameraError('Failed to analyze camera feed.');
    }
  };

  const handleVerifyMatch = (personData) => {
    alert(`Match verified! Police notified for person: ${personData.name}`);
    // Call backend to notify police if needed
    // You can send an API call to notify police with the person data here
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
      // Call to start analyzing the camera feed
      // handleAnalyzeCamera(); // Uncomment this to start analysis immediately
    } catch (error) {
      setCameraError('Failed to access the camera. Please allow camera access.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token'); // Remove token on logout
    setIsChatbotVisible(false); // Hide chatbot on logout
    navigate('/'); // Navigate to home or login page
  };
const generateReportID = (index, reportType) => {
    return reportType === 'person' ? `PERSON_${index + 1}` : `OBJECT_${index + 1}`;
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
            {missingReports.map((report, index) => (
              <div className="report-card" key={report.id}>
             <p><strong>Report ID:</strong> {generateReportID(index, report.type)}</p>
                <p><strong>Type:</strong> {report.type === 'person' ? 'Missing Person' : 'Missing Object'}</p>
                {report.type === 'person' && (
                  <>
                    <p><strong>Name:</strong> {report.name}</p>
                    <p><strong>Gender:</strong> {report.gender}</p>
                    <p><strong>Age:</strong> {report.age} years old</p>
                    <p><strong>Phone:</strong> {report.phoneNumber}</p>
                  </>
                )}
                <p><strong>Last Seen/Location:</strong> {report.location}</p>
                <p><strong>Description:</strong> {report.description}</p>

                {/* Image */}
                {report.imageUrl && (
                  <img
                    src={report.imageUrl}
                    alt={report.name || "Missing Report Image"}
                    style={{ width: '150px', height: '150px', objectFit: 'cover' }}
                  />
                )}
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
          contentLabel="How to Use Instructions"
          className="modal-content"
          overlayClassName="modal-overlay"
        >
          <h2>How to Use the Dashboard</h2>
	  <div class="video-container">
        <iframe
            width="813"
            height="419"
            src="https://www.youtube.com/embed/ocWosSs4PYA"
            title="1790 V2 Team name error404, Team ID-35761"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerpolicy="strict-origin-when-cross-origin"
            allowfullscreen>
        </iframe>
    </div>
          <ul className="instructions-list">
            <li>View the missing persons reports by clicking "View Missing Reports".</li>
            <li>Analyze the camera feed for potential matches by clicking "View Camera Feed".</li>
            <li>If a match is found, verify the match and notify the police.</li>
            <li>You can always access this help section by clicking "How to Use".</li>
          </ul>
          <button className="close-modal-btn" onClick={closeHowToUseModal}>Close</button>
        </Modal>
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
          <h2>Confirm Logout</h2>
          <p>Are you sure you want to logout?</p>
          <button className="confirm-logout-btn" onClick={handleLogout}>Yes, Logout</button>
          <button className="cancel-logout-btn" onClick={closeLogoutModal}>Cancel</button>
        </Modal>
      </div>
    </div>
  );
};

export default StaffDashboard;

