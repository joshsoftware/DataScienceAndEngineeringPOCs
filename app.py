from flask import Flask, request, jsonify
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from vector_store import QdrantDataLoader
from llm import response_generator
import os

load_dotenv()
qdrant_api = os.getenv("Qdrant_API")
qdrant_url = os.getenv("Qdrant_URL")

app = Flask(__name__)

# Load data endpoint
@app.route('/loaddata', methods=['GET'])
def loaddata():
    documents = SimpleDirectoryReader("C:/Data").load_data()
    data_loader = QdrantDataLoader(qdrant_api, qdrant_url)
    data_loader.load_data(documents)
    return jsonify({"text": "success"})

# Generate response endpoint
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_query = data.get('query')
    
    if user_query is None:
        return jsonify({"error": "Query parameter 'query' is required."}), 400
    
    loader = QdrantDataLoader(qdrant_api, qdrant_url)
    try:
        response_stream = response_generator(user_query, loader)
        return jsonify({"results": response_stream})
    except ValueError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
