from db.schema import ScrapData
from db.index import UserSession


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
