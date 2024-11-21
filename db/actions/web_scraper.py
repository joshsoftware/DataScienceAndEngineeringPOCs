from db.schema import ScrapData
from db.index import UserSession
from typing import Annotated
from fastapi import Query
from sqlmodel import select

def save_webscrap(data: dict, session: UserSession) -> ScrapData:   
    scrap_data = ScrapData(
        websiteUrl=data['websiteUrl'],
        websiteDepth=data['websiteDepth'],
        websiteMaxNumberOfPages=data['websiteMaxNumberOfPages'],
        lastScrapedDate=data['lastScrapedDate'],
        filePath=data['filePath']
    )
    
    session.add(scrap_data)
    session.commit()
    session.refresh(scrap_data)
    return scrap_data

def list_webscraps(
    session: UserSession,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[ScrapData]:
    heroes = session.exec(select(ScrapData).offset(offset).limit(limit)).all()
    return heroes

    