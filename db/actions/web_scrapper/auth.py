from db.actions.web_scrapper.model.user import UserLoginModel
from db.schema import UserDetails
from db.index import UserSession
from jose import jwt, JWTError
import os
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Union, Any

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES =os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES =os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")
ALGORITHM =os.getenv("ALGORITHM")
JWT_SECRET_KEY =os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY =os.getenv("JWT_REFRESH_SECRET_KEY")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def login(data: UserLoginModel, session: UserSession) -> UserDetails:
    try: 
        user = session.execute(select(UserDetails).where(UserDetails.email == data.email)).scalar()
        if user is None:
            raise HTTPException(status_code=400, detail="Use not found...")
        
        # if not verify_password(data.password, user.hashed_password):
        #     raise HTTPException(
        #         status_code=400, 
        #         detail="Wrong Email or Password"
        #     )
        # return {f"lll {user}"}

        access = create_access_token(user)
        refresh = create_refresh_token(user)
        
        return {
            "access_token": access,
            "refresh_token": refresh,
        }

    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database operation failed. Please try again. {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
        return payload
    
    except JWTError as e:
        print("Token verification failed:", e)
        return {"error": "Invalid token"}
    
def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
        
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
         
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
     
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:   
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt