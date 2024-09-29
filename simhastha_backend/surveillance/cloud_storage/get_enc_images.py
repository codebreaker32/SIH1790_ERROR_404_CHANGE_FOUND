import os
import json
from google.cloud import storage

# Set up Google Cloud Storage
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'simhastha_backend\keys\keys.json'  # Update this path

bucket_name = "face-recognition-sih1790"
encoded_images_file = "encoded-images.json"

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

if __name__ == "__main__":
    encoded_images = load_json_from_bucket(encoded_images_file)
    print(encoded_images)


## make sure that you use report id to get the images and not the whole list of images

## the data we get is None type, bas show ho rha hai no output
## generate output once the match has been found then use the signals.py to send the sms to the user


## 