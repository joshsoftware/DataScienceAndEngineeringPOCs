from db.schema import ScrapData
from db.index import UserSession
from typing import Annotated
from fastapi import Query
from sqlmodel import select


def list_webscraps(
    session: UserSession,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[ScrapData]:
    webscraps = session.exec(select(ScrapData).offset(offset).limit(limit)).all()
    return webscraps
