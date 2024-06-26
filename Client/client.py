import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

def generate_result(code_obj):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))

    prompt = f"""
    Analyze the following code based on the provided details and rate it on different factors:
    
    Code Language: {code_obj['language']}
    Code Answer: {code_obj['submitted_code']}
    Code Question: {code_obj['problem_statement']}
    Difficulty Level: {code_obj['difficulty_level']}
    Code ID: {code_obj['id']}

    Provide ratings out of 10 for the following factors:
    1. submission_id:{code_obj['id']}
    2. Logic of code
    3. Time Complexity
    4. Space Complexity
    5. Answer aligned with Question
    6. Optimality of the code

    Format the response only as:
    submission_id : code_id
    Logic of code: V/10
    Time Complexity: W/10
    Space Complexity: X/10
    Answer aligned with Question: Y/10
    Optimality of the code: Z/10
    """
    print("\n\nPrompt:\n\n", prompt)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=1.0,
        model="gpt-4o",
    )
    
    if chat_completion.choices:
        response_data = {
            "Results": chat_completion.choices[0].message.content,
        }
    else:
        response_data = {"Results": "No response generated"}

    #print(response_data)
    return response_data
