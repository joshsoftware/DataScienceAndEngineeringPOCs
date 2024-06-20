
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

def response_generator(user_query,loader):
    Settings.llm = Ollama(model="llama3")
    if loader.index is None:
        raise ValueError("Index is not loaded. Call load_data first.")
    query_engine = loader.index.as_query_engine(streaming=False, similarity_top_k=3)
    response_stream = query_engine.query(user_query)
    return response_stream