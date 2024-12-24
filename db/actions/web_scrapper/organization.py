from sqlmodel import select
from db.actions.web_scrapper.model.user import GetOrgModel, ScrapModel, UpdateOrgnizationModel
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

def update_organization(organization_domain: str, data: UpdateOrgnizationModel, session: UserSession ):
    try:
        org = session.execute(select(Orgnization).where(Orgnization.websiteDomain == organization_domain)).scalar()

        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        org.websiteUrl = data.url or org.websiteUrl
        org.websiteDomain = data.domain or org.websiteDomain
        org.websiteMaxNumberOfPages = data.max_pages or org.websiteMaxNumberOfPages
        org.websiteDepth = data.depth or org.websiteDepth
        org.websiteFrequency = data.frequency or org.websiteFrequency

        session.commit()
        session.refresh(org)
        return org

    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database operation failed. Please try again. {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
def get_organization(domain: str, session: UserSession) -> Orgnization:
    try:
        org_data = session.execute(select(Orgnization).where(Orgnization.websiteDomain == domain)).scalar()       
        return org_data
        
    except HTTPException as e:
        raise e
    
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database operation failed. Please try again. {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")