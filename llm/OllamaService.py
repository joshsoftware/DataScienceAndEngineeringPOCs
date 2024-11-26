from ollama import AsyncClient
from typing import List
from db.index import UserSession
from db.actions.vectors import get_similar_vectors
from .ChatHistory import ChatHistory
from ollama import AsyncClient
from typing import AsyncGenerator


async def ollama_client(query: str, session: UserSession) -> AsyncGenerator[dict, None]:
    if not hasattr(session, 'chat_history'):
        session.chat_history = ChatHistory()
    
    session.chat_history.add_message({'role': 'user', 'content': query})
    
    # need to convert the query text to a embeddings vector for searching
    # when implemented replace the below line with the actual generated vector
    query_vector = [0.1, 0.2, 0.3]  
    similar_vectors = await get_similar_vectors(query_vector, session)
    
    for vector in similar_vectors:
        metadata_str = str(vector['metaData'])
        session.chat_history.add_message({'role': 'system', 'content': metadata_str})
    
    context = session.chat_history.get_history()
    messages = [{'role': msg['role'], 'content': msg['content']} for msg in context]
    
    try:
        client = AsyncClient()
        async for chunk in await client.chat(
            model='llama3.2',  
            messages=messages,
            stream=True
        ):
            yield chunk
    except Exception as e:
        yield {'message': {'content': f"Error: {str(e)}"}}