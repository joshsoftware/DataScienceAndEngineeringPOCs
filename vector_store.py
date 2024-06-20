from qdrant_client import QdrantClient
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext, VectorStoreIndex, Settings

class QdrantDataLoader:
    def __init__(self, qdrant_api, qdrant_url):
        self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api)
        self.index = None
    
    def load_data(self, documents):
        embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
        Settings.embed_model = embed_model
        Settings.chunk_size = 512
        vector_store = QdrantVectorStore(client=self.client, collection_name="test3")
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self.index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
