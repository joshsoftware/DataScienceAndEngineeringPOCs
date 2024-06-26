import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify
import client
import json
import concurrent.futures
from App import db_utils
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

app = Flask(__name__)

@app.route('/')
def greet():
    return "Welcome to Code Analyzer!"

@app.route('/analyze')
def analyze():
    try:
        cur = conn.cursor()
        cur.execute("SELECT submission_id, problem_statement, submitted_code, language, level FROM submission")
        submissions = cur.fetchall()
        cur.close()
        
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_submission = {executor.submit(client.generate_result, {
                'id': submission[0],
                'problem_statement': submission[1],
                'submitted_code': submission[2],
                'language': submission[3],
                'difficulty_level': submission[4]
            }): submission for submission in submissions}

            for future in concurrent.futures.as_completed(future_to_submission):
                submission = future_to_submission[future]
                try:
                    result = future.result()
                    results.append(result)
                    # Parse and insert evaluation result into the evaluation table
                    response_data = result["Results"]
                    lines = response_data.split('\n')
                    scores = {line.split(":")[0].strip(): int(line.split(":")[1].strip().split('/')[0]) for line in lines if ":" in line}

                    db_utils.insert_evaluation(
                        submission_id=submission[0],  # Make sure submission[0] contains the submission_id
                        logic_score=scores.get('Logic of code'),
                        time_complexity_score=scores.get('Time Complexity'),
                        space_complexity_score=scores.get('Space Complexity'),
                        alignment_score=scores.get('Answer aligned with Question'),
                        optimality_score=scores.get('Optimality of the code')
                    )

                except Exception as exc:
                    print(f'{submission[0]} generated an exception: {exc}')
                    results.append({"submission_id": submission[0], "error": str(exc)})
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=6000)
