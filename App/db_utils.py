import psycopg2
import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

def update_submission(submission_id, data):
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE submission SET problem_statement = %s::jsonb, submitted_code = %s::jsonb, language = %s, level = %s, received_at = %s WHERE submission_id = %s",
            (json.dumps(data['problem_statement']), json.dumps(data['submitted_code']), data['language'], data['difficulty_level'], datetime.datetime.now(), str(submission_id))
        )
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        conn.rollback()  # rollback in case of error
        raise e

def insert_submission_ids(submission_ids, drive_id):
    try:
        cur = conn.cursor()
        cur.executemany(
            "INSERT INTO submission (submission_id, drive_id, submission_datetimestamp) VALUES (%s, %s, %s)",
            [(submission_id, drive_id, datetime.datetime.now()) for submission_id in submission_ids]
        )
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        conn.rollback()  # rollback in case of error
        raise e

def get_submissions_for_analysis():
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, problem_statement, language, level, submitted_code FROM submission")
        rows = cur.fetchall()
        cur.close()

        submissions = []
        for row in rows:
            submissions.append({
                "submission_id": row[0],
                "problem_statement": row[1],
                "language": row[2],
                "difficulty_level": row[3],
                "submitted_code": row[4]
            })

        return submissions
    except psycopg2.Error as e:
        raise e

def insert_evaluation(submission_id, logic_score, time_complexity_score, space_complexity_score, alignment_score, optimality_score):
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO evaluation (submission_id, logic_score, time_complexity_score, space_complexity_score, alignment_score, optimality_score) VALUES (%s, %s, %s, %s, %s, %s)",
            (submission_id, logic_score, time_complexity_score, space_complexity_score, alignment_score, optimality_score)
        )
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        conn.rollback()  # rollback in case of error
        raise e
