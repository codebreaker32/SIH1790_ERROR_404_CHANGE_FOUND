import os
import json
import cv2
import numpy as np
from google.cloud import storage
from google.cloud import vision
import face_recognition
import subprocess 

# Set the environment variable for Google Cloud Vision API key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"key.json"  # Replace with your file path

# Initialize Google Cloud Vision client
client = vision.ImageAnnotatorClient()

# Load encoded faces and labels from encoded-images.json
bucket_name = "face-recognition-sih1790"
encoded_images_file = "encoded-images.json"

def load_encoded_faces_from_bucket(bucket_name, blob_name):
    """Load the encoded faces from the specified blob in the bucket."""
    # Initialize Google Cloud Storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    if blob.exists():
        # Download and load JSON data
        encoded_data = blob.download_as_text()
        return json.loads(encoded_data)
    else:
        print(f"{blob_name} not found in the bucket.")
        return {}

# Load known face encodings and labels
encoded_faces_data = load_encoded_faces_from_bucket(bucket_name, encoded_images_file)

known_face_encodings = []
known_face_labels = []

for label, encoding in encoded_faces_data.items():
    known_face_encodings.append(encoding)
    known_face_labels.append(label)

# Initialize webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture a frame from the webcam
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Convert the frame to bytes for Google Vision API
    _, encoded_image = cv2.imencode('.jpg', frame)
    content = encoded_image.tobytes()

    # Prepare the image for Google Vision API
    image = vision.Image(content=content)

    # Perform face detection
    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Check for errors in the response
    if response.error.message:
        print(f"Error processing frame: {response.error.message}")
        continue

    # Track matched faces and their corresponding labels
    matched_faces = []

    # Draw rectangles around detected faces and check for matches
    for face in faces:
        vertices = [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]

        # Convert the detected face region to a format suitable for face_recognition
        face_image = frame[vertices[0][1]:vertices[2][1], vertices[0][0]:vertices[2][0]]
        face_image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        face_encoding = face_recognition.face_encodings(face_image_rgb)

        if face_encoding:
            face_encoding = face_encoding[0]

            # Compare with known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            if True in matches:
                match_index = matches.index(True)
                match_label = known_face_labels[match_index]
                matched_faces.append((vertices, match_label))  # Store matched face vertices and label

    # Draw rectangles and labels only for matched faces
    for vertices, match_label in matched_faces:
        # Draw a thin blue rectangle
        cv2.polylines(frame, [np.array(vertices)], isClosed=True, color=(255, 0, 0), thickness=1)  # Blue rectangle
        
        # Put the label on the bounding box with black color
        label_position = (vertices[0][0], vertices[0][1] - 10)  # Adjust position to be above the box
        cv2.putText(frame, match_label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)  # Black label

    # Display the result
    cv2.imshow('Video', frame)

    # Press 'q' to quit the webcam feed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
video_capture.release()
cv2.destroyAllWindows()



# Uncomment at actual deployment

# subprocess.run("python","clear.py")