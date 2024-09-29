import redis
import random
from django.conf import settings
import requests
import logging
from django.utils import timezone
from datetime import datetime
from decouple import config

# Initialize Redis connection
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

def send_otp(phone_number):
    # Get the API key from environment variables
    api_key = config('API_KEY_2FACTOR', default='d9cdc6f2-7c35-11ef-8b17-0200cd936042')
    
    otp = random.randint(100000, 999999)  # Generate OTP
    expiry_time = 300  # 5 minutes in seconds

    # Store OTP and timestamp in Redis
    r.setex(f"otp_{phone_number}", expiry_time, otp)
    otp_created_at = timezone.now().isoformat()
    r.setex(f"otp_{phone_number}_created", expiry_time, otp_created_at)

    # Send the OTP using 2Factor API
    # url = f"https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}/AUTOGEN"
    
    # response = requests.get(url)
    # if response.status_code == 200:
    #     return otp  # Success
    # else:
    #     raise Exception(f"Failed to send OTP: {response.text}")
    return otp

def verify_otp(phone_number, otp_entered):
    # Retrieve OTP and created time from Redis
    print("Checking if data was stored in Redis...")
    stored_otp = r.get(f"otp_{phone_number}")
    stored_time = r.get(f"otp_{phone_number}_created")

    if not stored_otp:
        print("No OTP found for the provided phone number in Redis.")
        return False, "OTP has expired. Please request a new one."

    if not stored_time:
        print("No stored time found for the provided phone number in Redis.")
        return False, "Stored time not found. Please request a new OTP."

    try:
        stored_time_str = stored_time.decode()
        print(f"Stored time in Redis: {stored_time_str}")

        stored_time = datetime.fromisoformat(stored_time_str)

        if timezone.is_naive(stored_time):
            print("Stored time is naive, making it timezone-aware.")
            stored_time = timezone.make_aware(stored_time)
    except ValueError as e:
        print(f"Error parsing stored_time: {e}")
        return False, "Invalid stored time format."

    # Compare stored OTP with the entered OTP
    if stored_otp.decode() == str(otp_entered):
        return True, "OTP verified successfully."
    else:
        return False, "Incorrect OTP entered."
