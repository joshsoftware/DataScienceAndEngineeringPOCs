from db.actions.web_scrapper.model.user import UserModel
from db.schema import UserDetails
from db.index import UserSession
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(data: UserModel, session: UserSession) -> UserDetails:  
    try:
        existing_user = session.execute(select(UserDetails).where(UserDetails.email == data.email)).scalar()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        user_data = UserDetails(
            name=data.name,
            email=data.email,
            domain=data.domain,
            contact_number=data.contactNumber,
            hashed_password= password_context.hash(data.password) ,
        )
    
        session.add(user_data)
        session.commit()
        session.refresh(user_data)
        return user_data
    
    except HTTPException as e:
        raise e
    
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database operation failed. Please try again. {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
