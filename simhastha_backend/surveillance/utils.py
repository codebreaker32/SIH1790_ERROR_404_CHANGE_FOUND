import os
import json
from google.cloud import storage
from django.core.signals import Signal
from django.dispatch import receiver

# Set up Google Cloud Storage
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'simhastha_backend/keys/keys.json'  # Ensure path is correct

bucket_name = "face-recognition-sih1790"
missing_persons_folder = "missing persons"
encoded_images_file = "encoded-images.json"

# Initialize Google Cloud Storage client
client = storage.Client()
bucket = client.bucket(bucket_name)

# Custom signal for sending SMS when a match is found
match_found_signal = Signal(providing_args=["phone_number", "report_id"])

def save_image_to_missing_persons(image_data, label):
    """
    Save an image to the missing persons folder in the Google Cloud bucket.
    
    :param image_data: Binary data of the image to upload.
    :param label: The label used to save the image (e.g., report_id).
    :return: The public URL of the uploaded image.
    """
    try:
        # Create a blob for the image with a label (report_id)
        blob_name = f"{missing_persons_folder}/{label}.jpg"
        blob = bucket.blob(blob_name)
        
        # Upload the image data to Google Cloud Storage
        blob.upload_from_string(image_data, content_type='image/jpeg')

        print(f"Image saved to {blob_name}.")
        return blob.public_url
    except Exception as e:
        print(f"Error saving image {label}: {e}")
        return None


def load_json_from_bucket(blob_name):
    """
    Load JSON data from a specified blob in the Google Cloud bucket.
    
    :param blob_name: The name of the blob containing JSON data.
    :return: Parsed JSON data or an empty dictionary if the blob doesn't exist or fails to load.
    """
    try:
        blob = bucket.blob(blob_name)
        if blob.exists():
            data = blob.download_as_text()
            return json.loads(data)
        else:
            print(f"Blob {blob_name} does not exist.")
            return {}
    except Exception as e:
        print(f"Error loading {blob_name}: {e}")
        return {}


def get_encoded_image_by_report_id(report_id):
    """
    Get the encoded image data for a specific report ID.
    
    :param report_id: The unique report ID used to retrieve the image.
    :return: Encoded image data or None if not found.
    """
    encoded_images = load_json_from_bucket(encoded_images_file)
    
    # Retrieve encoded image for the specific report_id
    if report_id in encoded_images:
        return encoded_images[report_id]
    else:
        print(f"No encoded image found for report_id: {report_id}")
        return None


# Signal receiver to send SMS notification when a match is found
@receiver(match_found_signal)
def send_sms_on_match(phone_number, report_id, **kwargs):
    """
    Send SMS to the user when a match is found.
    
    :param phone_number: The phone number to send the SMS to.
    :param report_id: The report ID related to the match.
    """
    try:
        # Use Twilio or any SMS service here to send an SMS
        # This is a placeholder print statement to simulate the SMS
        print(f"SMS sent to {phone_number} regarding match with report ID: {report_id}")
    except Exception as e:
        print(f"Error sending SMS: {e}")
