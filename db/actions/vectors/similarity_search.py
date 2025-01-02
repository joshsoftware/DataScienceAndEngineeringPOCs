from typing import List, Any
from db.schema import OrgDataEmbedding
from sqlmodel import select, cast, String, or_
from db.index import UserSession

async def get_similar_vectors(query_vector: List[float], orgnization_id:int, session: UserSession, top_k: int = 5   ) -> List[Any]:
    try:
        result = session.exec(
                    select(OrgDataEmbedding)
                    .where(OrgDataEmbedding.org_id == orgnization_id)
                    .where(OrgDataEmbedding.embedding.l2_distance(query_vector) <= 1)
                    .order_by(OrgDataEmbedding.embedding.l2_distance(query_vector))
                    .limit(top_k))
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


async def search_by_keywords( keywords: List[str], organization_id: int,  session: UserSession, limit: int = 5) -> List[Any]:
    """
    Search rows by matching keywords in metadata['sentence']
    
    Args:
        keywords: List of search keywords
        organization_id: Organization ID
        session: Database session
        limit: Maximum results to return
        
    Returns:
        List of matching records with id, metadata and embedding
    """
    try:
        keywords = [k.lower().strip() for k in keywords]
        search_conditions = [
            cast(OrgDataEmbedding.metaData['sentence'], String).ilike(f'%{k}%')
            for k in keywords
        ]
        
        result = session.exec(
            select(OrgDataEmbedding)
            .where(OrgDataEmbedding.org_id == organization_id)
            .where(or_(*search_conditions))
            .limit(limit)
        )
        
        rows = result.all()
        formatted_rows = [{
            "id": row.id,
            "metaData": row.metaData,
            "embedding": row.embedding.tolist()
        } for row in rows]
        
        return formatted_rows
        
    finally:
        session.close()