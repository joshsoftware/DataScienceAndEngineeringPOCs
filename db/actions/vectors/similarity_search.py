from typing import List, Any
from db.schema import VectorData
from sqlmodel import select
from db.index import UserSession

async def get_similar_vectors(query_vector: List[float], session: UserSession, top_k: int = 5) -> List[Any]:
    try:
        result = session.exec(select(VectorData).order_by(VectorData.embedding.l2_distance(query_vector)).limit(top_k))
        rows = result.all()
        formatted_rows = [
            {
                "id": row.id,
                "metaData": row.metaData,
                "embedding": row.embedding.tolist()
            }
            for row in rows
        ]
        return formatted_rows
    finally:
        session.close()