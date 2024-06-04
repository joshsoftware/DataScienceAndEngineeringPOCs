import requests
import json

#submission ids
submission_ids = [22, 24, 37, 30, 34, 43]

# Flask app url
flask_app_url = 'http://127.0.0.1:5000'

submission_route = '/submissions_ids'

headers = {'Content-Type': 'application/json'}
data = {'submission_ids': submission_ids, 'drive_id': '110'}

try:
    response = requests.post(f"{flask_app_url}{submission_route}", json=data, headers=headers)

    if response.status_code == 200:
        print('Submission IDs and drive ID sent to Flask app successfully')
    else:
        print(f"Failed to send Submission IDs and drive ID to Flask app: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
