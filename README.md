This README provides an overview of the project, including team details, relevant links, tasks completed, tech stack, key features, and steps to run the project locally.


## About Project
1. Real-Time Face Recognition: The system automates the identification of missing persons using real-time face recognition with live video feeds, speeding up the detection process.
2. Enhanced Communication: Twilio is used for sending instant notifications to police and families when a match is detected.
3. Image Enhancement: GFPGAN is used to improve the quality of images uploaded by users to ensure accurate identification.
4. Live Video Monitoring: The system monitors live video feeds and continuously compares detected faces with stored data for potential matches.
5. Centralized Dashboard: Police can access missing person reports, live video feeds, and receive alerts in real-time from their dashboard.
6. Scalable System: The system architecture is built to handle the scale of events like Simhastha Ujjain, where millions of people are present, ensuring no delay in processing large amounts of data.
7. User-Friendly Interface: Both users and police staff have easy-to-use interfaces for filing reports and monitoring alerts, designed for high accessibility and ease of use.


## Team Details

**Team Name:** ERROR 404 : CHANGE FOUND?

**Project Title** -Face Recognition Surveillance System and Communication Systems for Missing Persons or Items at Simhastha Ujjain 

**Team Leader:** [@HARSHDIPSAHA](https://github.com/HARSHDIPSAHA)

**Team Members:**

- **ANSHUMAN RAJ** - 2023UCD3053 - [@SAVAGECAT05](https://github.com/SAVAGECAT05)
- **HEMANK KAUSHIK** - 2023UEI2867 - [@HEMANKKAUSHIK](https://github.com/HEMANKKAUSHIK)
- **KANISHK SHARMA** - 2023UCD2175 - [@GHOSTDOG007](https://github.com/GHOSTDOG007)
- **ANSHIKA SINGH** - 2023UCA1946 - [@CUBIX33](https://github.com/CUBIX33)
- **HARSHDIP SAHA** - 2023UCA1897 - [@HARSHDIPSAHA](https://github.com/HARSHDIPSAHA)
- **AMAN BIHARI** - 2023UCA1910 - [@CODEBREAKER32](https://github.com/CODEBREAKER32)

**Live Deployment:** [View Deployment](https://willowy-toffee-89c6b8.netlify.app/)
  (backend deployment is removed due to insufficient aws credits)

  
**Run locally**
## Local Setup Instructions (Write for both windows and macos)

Follow these steps to run the project locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/HARSHDIPSAHA/SIH1648_ERROR_404_CHANGE_FOUND
   cd REPO_DIRECTORY
   ```

## Django Backend 

This project is a Django-based backend for managing diabetes patient data, providing user authentication, patient data handling, and integration with machine learning models for outcome predictions and recommendations.
### 1. Clone the repository
 ```bash
git clone <https://github.com/HARSHDIPSAHA/SIH1648_ERROR_404_CHANGE_FOUND>
```
### 2. Create and activate a virtual environment
 ```bash
python3 -m venv venv
source venv/bin/activate
``` 
For Windows, use `venv\Scripts\activate`

### 3. Install the dependencies
 ```bash
pip install -r requirements.txt
```
### 4. Setup the Django project (migrate database and create superuser)
 ```bash
python manage.py migrate
```
### 5. Start the development server
 ```bash

python manage.py createsuperuser
```
### 6. Run the server
 ```bash
python manage.py runserver
```
## REACT FRONTEND 
### Prerequisites
- Node.js (v14.x or later)
- npm (v6.x or later) or yarn.

## Setup instructions 

### 1. Clone the repository 
```bash
git clone <https://github.com/HARSHDIPSAHA/SIH1648_ERROR_404_CHANGE_FOUND>

```
### 2. Install the dependencies 
 ```bash
npm install
npm install react-scripts 
npm install react-router-dom
```
### 3. Start the development server
```bash
npm start
```
### 4. Build for production (optional)
 ```bash
npm run build
```
### 5. For Backend Integration 
```bash 
npm install axios


