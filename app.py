from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/')
def index():
    pass


if __name__ == '__main__':
    app.run(debug=True)