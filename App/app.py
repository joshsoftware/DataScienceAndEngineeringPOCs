import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify, request
from custom_auth import hmac_auth_required
import requests
import db_utils
import concurrent.futures
from Client.client import generate_result
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set your secret key here
app.config['HMAC_KEY'] = os.getenv("HMAC_KEY")

MOCK_SERVER = os.getenv("MOCK_SERVER")

@app.route('/get_submission/<int:submission_id>', methods=['GET'])
@hmac_auth_required
def get_submission(submission_id):
    try:
        response = requests.get(f"{MOCK_SERVER}{submission_id}")
        data = response.json()

        if response.status_code == 200:
            db_utils.update_submission(submission_id, data['data'])
            return jsonify(data['data']), 200
        else:
            return jsonify({'error': 'Failed to fetch data from mock server'}), 500
    except Exception as e:
        app.logger.error(f"Error fetching data from mock server: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/submissions_ids', methods=['POST'])
@hmac_auth_required
def submissions_ids():
    try:
        data = request.get_json()
        submission_ids = data['submission_ids']
        drive_id = data['drive_id']

        db_utils.insert_submission_ids(submission_ids, drive_id)

        # Fetching details for each submission_id
        for submission_id in submission_ids:
            response = requests.get(f"{MOCK_SERVER}{submission_id}")
            if response.status_code == 200:
                get_submission(submission_id)
            else:
                app.logger.error(f"Failed to fetch data from mock server for submission ID: {submission_id}")

        return jsonify({'message': 'Ids received and data fetched'}), 200
    except Exception as e:
        app.logger.error(f"Error inserting submission IDs: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_submissions', methods=['POST'])
@hmac_auth_required
def analyze_submissions():
    try:
        submissions = db_utils.get_submissions_for_analysis()

        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_code = {executor.submit(generate_result, code): code for code in submissions}
            for future in concurrent.futures.as_completed(future_to_code):
                code = future_to_code[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Parse the result and store it in the evaluation table
                    parsed_result = db_utils.parse_evaluation_result(result)
                    db_utils.insert_evaluation(parsed_result)
                except Exception as exc:
                    app.logger.error(f'{code["submission_id"]} generated an exception: {exc}')
                    results.append({"submission_id": code["submission_id"], "error": str(exc)})

        return jsonify(results), 200
    except Exception as e:
        app.logger.error(f"Error analyzing submissions: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
