from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()
qdrant_api = os.getenv("Qdrant_API")
qdrant_url = os.getenv("Qdrant_URL")

client = QdrantClient(
    url= qdrant_url,
    api_key=qdrant_api,
)