from flask import Flask, jsonify, request
import requests
import psycopg2
import datetime

app = Flask(__name__)

conn = psycopg2.connect(
    host="localhost",
    database="code_analyzer",
    user="postgres",
    password="Josh@123"
)

MOCK_SERVER = 'http://127.0.0.1:8787/api/submissions/'

@app.route('/get_submission/<int:submission_id>', methods=['GET'])
def get_submission(submission_id):
    try:
        response = requests.get(f"{MOCK_SERVER}{submission_id}")
        data = response.json()

        if response.status_code == 200:
            cur = conn.cursor()

            # Updating db
            cur.execute(
                "UPDATE submission SET problem_statement = %s, submitted_code = %s, language = %s, level = %s, received_at = %s WHERE submission_id = %s",
                (data['data']['problem_statement'], data['data']['submitted_code'], data['data']['language'], data['data']['difficulty_level'], datetime.datetime.now(), str(submission_id))
            )

            conn.commit()
            cur.close()

            return jsonify(data['data']), 200
        else:
            return jsonify({'error': 'Failed to fetch data from mock server'}), 500
    except psycopg2.Error as e:
        conn.rollback()  # rollback in case of error
        app.logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        app.logger.error(f"Error fetching data from mock server: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/submissions_ids', methods=['POST'])
def submissions_ids():
    try:
        data = request.get_json()
        submission_ids = data['submission_ids']
        drive_id = data['drive_id']

        cur = conn.cursor()
        cur.executemany(
            "INSERT INTO submission (submission_id, drive_id, submission_datetimestamp) VALUES (%s, %s, %s)",
            [(submission_id, drive_id, datetime.datetime.now()) for submission_id in submission_ids]
        )
        conn.commit()
        cur.close()

        # Fetching details for each submission_id
        for submission_id in submission_ids:
            requests.get(f"http://127.0.0.1:5000/get_submission/{submission_id}")

        return jsonify({'message': 'Ids received and data fetched'}), 200
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Error inserting submission IDs: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
