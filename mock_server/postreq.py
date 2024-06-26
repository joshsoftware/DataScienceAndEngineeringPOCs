import requests
import json
import hmac
import hashlib
import base64
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_signature(secret_key, method, path, data):
    timestamp = str(int(time.time()))
    message = f"{method}{path}{timestamp}{json.dumps(data, separators=(',', ':'))}"
    signature = base64.urlsafe_b64encode(
        hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    ).decode()
    return signature, timestamp

# Submission IDs
submission_ids = [43, 22, 24, 37, 30, 34]

# Flask app URL
flask_app_url = os.getenv("FLASK_APP_URL")
submission_route = '/submissions_ids'

# Set your secret key here
secret_key = os.getenv("HMAC_KEY")

data = {'submission_ids': submission_ids, 'drive_id': '110'}
signature, timestamp = generate_signature(secret_key, 'POST', submission_route, data)

# Construct headers
headers = {
    'Content-Type': 'application/json',
    'X-SIGNATURE': signature,
    'X-TIMESTAMP': timestamp
}

try:
    response = requests.post(f"{flask_app_url}{submission_route}", json=data, headers=headers)

    if response.status_code == 200:
        print('Submission IDs and drive ID sent to Flask app successfully')
    else:
        print(f"Failed to send Submission IDs and drive ID to Flask app: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
