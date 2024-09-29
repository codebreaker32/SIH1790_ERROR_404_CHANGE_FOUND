import os
import json
import io  # Import io for handling bytes
import face_recognition
from google.cloud import storage

# Set up Google Cloud Storage
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\anni1\OneDrive\Desktop\face_recognition\face-recognition\key.json'  # Update this path

bucket_name = "face-recognition-sih1790"
encoded_images_file = "encoded-images.json"
missing_persons_folder = "missing persons"  # Adjust if the folder path is different

# Initialize Google Cloud Storage client
client = storage.Client()
bucket = client.bucket(bucket_name)

def load_json_from_bucket(blob_name):
    """Load JSON data from a specified blob in the bucket."""
    try:
        blob = bucket.blob(blob_name)
        if blob.exists():
            data = blob.download_as_text()
            return json.loads(data)
        else:
            return {}
    except Exception as e:
        print(f"Error loading {blob_name}: {e}")
        return {}

def save_json_to_bucket(blob_name, data):
    """Save JSON data to a specified blob in the bucket."""
    try:
        blob = bucket.blob(blob_name)
        blob.upload_from_string(json.dumps(data))
    except Exception as e:
        print(f"Error saving {blob_name}: {e}")

def load_faces():
    """Load faces from the missing persons folder and update the encoded images JSON."""
    # Load existing encoded images
    encoded_images = load_json_from_bucket(encoded_images_file)

    # Check if the missing persons folder is empty
    missing_persons_blobs = list(bucket.list_blobs(prefix=missing_persons_folder + '/'))
    
    if not missing_persons_blobs:
        print("Missing persons folder is empty.")
        return

    # Load faces from the missing persons folder
    for blob in missing_persons_blobs:
        if blob.name.endswith('/'):  # Skip directories
            continue
        
        # Load the image as bytes
        image_data = blob.download_as_bytes()
        
        # Load the image from bytes using io.BytesIO
        image = face_recognition.load_image_file(io.BytesIO(image_data))
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            # Generate a unique label (you may want to implement a better mechanism for generating unique labels)
            label = f"Person_{len(encoded_images) + 1}"

            # Add to the encoded images
            encoded_images[label] = face_encodings[0].tolist()  # Convert numpy array to list for JSON serialization

            # Remove the blob from the missing persons folder
            blob.delete()
            print(f"Processed and added {label} to encoded images.")
        else:
            print(f"No faces found in {blob.name}. Skipping.")

    # If encoded_images is empty, initialize it
    if not encoded_images:
        encoded_images = {}

    # Save the updated encoded images back to the bucket
    save_json_to_bucket(encoded_images_file, encoded_images)

if __name__ == "__main__":
    load_faces()
