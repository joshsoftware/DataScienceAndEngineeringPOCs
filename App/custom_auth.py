'''import hmac
import hashlib
import json
import base64
from functools import wraps
from flask import request, jsonify, current_app

def verify_hmac_auth(secret_key, method, path, signature, data):
    message = f"{method}{path}{json.dumps(data, separators=(',', ':'))}"
    expected_signature = base64.urlsafe_b64encode(
        hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    ).decode()
    print(f"Expected Signature: {expected_signature}")
    print(f"Provided Signature: {signature}")
    return hmac.compare_digest(expected_signature, signature)

def hmac_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        secret_key = current_app.config['HMAC_KEY']
        method = request.method
        path = request.path
        signature = request.headers.get('X-SIGNATURE')
        data = request.get_json()

        print(f"Method: {method}")
        print(f"Path: {path}")
        print(f"Signature: {signature}")
        print(f"Data: {data}")

        if not signature:
            return jsonify({'error': 'Missing authentication headers'}), 403

        if not verify_hmac_auth(secret_key, method, path, signature, data):
            return jsonify({'error': 'Invalid HMAC signature'}), 403

        return f(*args, **kwargs)
    return decorated_function'''

import hmac
import hashlib
import base64
import datetime
from functools import wraps
from flask import request, jsonify, current_app
import json

def verify_hmac_auth(secret_key, method, path, timestamp, signature, data):
    message = f"{method}{path}{timestamp}{json.dumps(data, separators=(',', ':'))}"
    print(message)
    expected_signature = base64.urlsafe_b64encode(
        hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    ).decode()
    return hmac.compare_digest(expected_signature, signature)


def hmac_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        secret_key = current_app.config['HMAC_KEY']
        method = request.method
        path = request.path
        timestamp = request.headers.get('X-TIMESTAMP')
        signature = request.headers.get('X-SIGNATURE')
        data = request.get_json()
        print("Before verifying the hmac")

        if not timestamp or not signature:
            return jsonify({'error': 'Missing authentication headers'}), 403

        if not verify_hmac_auth(secret_key, method, path, timestamp, signature, data):
            return jsonify({'error': 'Invalid HMAC signature'}), 403
        print("After verifying the hmac")
        return f(*args, **kwargs)
    return decorated_function
