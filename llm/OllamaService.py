from ollama import AsyncClient
from typing import List
from db.index import UserSession
from db.actions.vectors import get_similar_vectors, search_by_keywords
from .ChatHistory import ChatHistory
from ollama import AsyncClient
from typing import AsyncGenerator
from src.embeddings.service import EmbeddingService
from src.embeddings.sentenceSegmentation import SentenceSegmentationService


async def ollama_client(query: str, orgnization_id: int, session: UserSession) -> AsyncGenerator[dict, None]:
    if not hasattr(session, 'chat_history'):
        session.chat_history = ChatHistory()

    session.chat_history.add_message({'role': 'user', 'content': query})

    query_vector = await EmbeddingService().get_query_vector(query)

    similar_vectors = await get_similar_vectors(query_vector, orgnization_id, session)

    keywords = SentenceSegmentationService().extract_keywords(query)

    similar_vectors_by_keywords = await search_by_keywords(keywords, orgnization_id, session)

    vector_ids = {vector['id'] for vector in similar_vectors}
    keyword_vector_ids = {vector['id'] for vector in similar_vectors_by_keywords}

    filtered_ids = vector_ids.intersection(keyword_vector_ids)

    filtered_vectors = [
        vector for vector in similar_vectors if vector['id'] in filtered_ids
    ]

    if filtered_vectors:
        for vector in filtered_vectors:
            metadata_str = str(vector['metaData'])
            session.chat_history.add_message({'role': 'system', 'content': metadata_str})

        context = session.chat_history.get_history()
        messages = [{'role': msg['role'], 'content': msg['content']} for msg in context]

        print("Messages", messages)

        try:
            client = AsyncClient()
            async for chunk in await client.chat(
                model='llama3',  
                messages=messages,
                stream=True
            ):
                yield chunk
        except Exception as e:
            yield {'message': {'content': f"Error: {str(e)}"}}
    else:
        chunk = {
        "done": True,
        "done_reason": "stop",
        "message": {
            "content": "The query appears to be out of context please rephrase it",
        }
    }
    yield chunk