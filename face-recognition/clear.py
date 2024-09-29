import os
import json
import uuid
from google.cloud import storage

# Set the environment variable for Google Cloud Vision API key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"key.json"  # Replace with your file path

# Set the bucket name and file names
bucket_name = "face-recognition-sih1790"
encoded_images_file = "encoded-images.json"
processed_images_folder = "processed-images/"

def clear_encoded_images(bucket_name):
    """Clear the contents of encoded-images.json and push an empty file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Clear the contents of encoded-images.json locally
    with open(encoded_images_file, 'w') as file:
        json.dump({}, file)  # Writing an empty JSON object

    # Upload the cleared encoded-images.json to the bucket
    blob_empty = bucket.blob(encoded_images_file)
    blob_empty.upload_from_filename(encoded_images_file)  # Uploading the empty file

    # Create a unique ID for processed images
    unique_id = str(uuid.uuid4())

    # Rename and upload the original encoded-images.json as processed-images{uniqueID}.json
    processed_file_name = f"{processed_images_folder}processed-images-{unique_id}.json"
    blob_processed = bucket.blob(processed_file_name)

    # Read the original encoded-images.json and upload it with the new name
    with open(encoded_images_file, 'r') as original_file:
        encoded_data = original_file.read()
        blob_processed.upload_from_string(encoded_data)

    print(f"Cleared {encoded_images_file} and uploaded to bucket.")
    print(f"Original file uploaded as {processed_file_name}.")

if __name__ == "__main__":
    clear_encoded_images(bucket_name)
