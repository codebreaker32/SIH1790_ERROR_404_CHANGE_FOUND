import os
import json
from google.cloud import storage



# Set up Google Cloud Storage
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'simhastha_backend\keys\keys.json'  # Update this path

bucket_name = "face-recognition-sih1790"
missing_persons_folder = "missing persons"  # Adjust if the folder path is different

# Initialize Google Cloud Storage client
client = storage.Client()
bucket = client.bucket(bucket_name)

def save_image_to_missing_persons(image_data, label):
    """Save an image to the missing persons folder in the bucket."""
    try:
        # Create a blob for the image
        blob_name = f"{missing_persons_folder}/{label}.jpg"  # Save as JPG, adjust extension if needed
        blob = bucket.blob(blob_name)
        
        # Upload the image data
        blob.upload_from_string(image_data, content_type='image/jpeg')  # Specify the content type

        print(f"Image saved to {blob_name}.")
    except Exception as e:
        print(f"Error saving image {label}: {e}")

if __name__ == "__main__":
    # Example: Save an image (replace this with actual image data)
    with open(r"C:\Users\Anshuman Raj\OneDrive\Desktop\final_ps_1790\simhastha_backend\media\reports\WhatsApp_Image_2023-12-12_at_16.57.25_dc389121.jpg", "rb") as img_file:  # Update the path to your image
        image_data = img_file.read()
        save_image_to_missing_persons(image_data, "example_person")