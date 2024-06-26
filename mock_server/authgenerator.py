import hmac
import json
import hashlib
import base64
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_signature(secret_key, method, path, data):
    timestamp = str(int(datetime.datetime.now().timestamp()))
    message = f"{method}{path}{timestamp}{json.dumps(data, separators=(',', ':'))}"
    signature = base64.urlsafe_b64encode(
        hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    ).decode()
    print(f"Timestamp: {timestamp}")
    print(f"Signature: {signature}")
    return signature, timestamp

if __name__ == "__main__":
    secret_key = os.getenv("HMAC_KEY")
    method = 'POST'
    path = '/submissions_ids'
    data = {'submission_ids': [43, 22, 24, 37, 30, 34], 'drive_id': '110'}
    signature, timestamp = generate_signature(secret_key, method, path, data)
    