from sqlmodel import select
from db.actions.web_scrapper.model.user import ScrapModel
from db.schema import Orgnization
from db.index import UserSession
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

def register_organization(data: ScrapModel, session: UserSession) -> Orgnization:
    try:
        existing_org = session.execute(select(Orgnization).where(Orgnization.websiteDomain == data.domain)).scalar()
        if existing_org:
            raise HTTPException(status_code=400, detail="Organization already registered")
        
        org_data = Orgnization(
            user_id= data.user,
            websiteUrl=data.url,
            websiteDomain = data.domain,
            websiteMaxNumberOfPages=data.max_pages,
            websiteDepth=data.depth,
            websiteFrequency=data.frequency
        )
    
        session.add(org_data)
        session.commit()
        session.refresh(org_data)
        return org_data
    
    except HTTPException as e:
        raise e
    
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database operation failed. Please try again. {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

