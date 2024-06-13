from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "HR-Bot is Running..... "

@app.route('/generate', methods= ['POST'])
def generate ():
    data = request.json
    return data

if __name__ == '__main__':
    app.run(debug=True)