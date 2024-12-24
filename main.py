from db.actions.web_scrapper.model.user import GetOrgModel, ScrapModel, UpdateOrgnizationModel, UserLoginModel, UserModel
from db.actions.web_scrapper.model.organization import ScrapModel
from db.schema import Orgnization
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from data_source.webscraper.index import WebCrawler
from db.index import create_db_and_tables, UserSession
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from db.actions.vectors import get_similar_vectors
from db.actions.web_scrapper import list_webscraps, save_webscrap, auth, users, organization
#from db.actions.embeddings import save_embeddings
from llm.OllamaService import ollama_client
from llm.ChatHistory import ChatHistory
import json


from typing import List, AsyncGenerator
# class ScrapModel(BaseModel):
#     base_url: HttpUrl = Field(..., example="https://example.com")
#     depth: int = Field(..., ge=1, le=10, example=3)
#     max_pages: int = Field(..., gt=0, example=2)

class VectorQueryModel(BaseModel):
    query_vector: List[float] = Field(..., example=[0.1, 0.2, 0.3])
    top_k: int = Field(5, example=5)
    
class ChatModel(BaseModel):
    message: str = Field(..., example="Hello, Ollama!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan,debug=True)

# Add CORS middleware
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/web-scrap/")
async def get_webscrap(session: UserSession):
    return list_webscraps(session)

@app.get("/vector-query/")
async def vector_query(session: UserSession):
    results = await get_similar_vectors([0.09,0.019,0.029], session)
    return results

@app.post("/web-scrap/")
async def scrap_website(scrap_model: ScrapModel, session: UserSession):
    crawler = WebCrawler(str(scrap_model.base_url), depth=scrap_model.depth, max_pages=scrap_model.max_pages)
    crawler.crawl()
    data = crawler.save_results()
    org_data = save_webscrap(data, session)
    print("data: ", data)
    #await save_embeddings(org_data, session)
    return {"message": "Crawling completed successfully"}

@app.post("/chat")
async def chat_endpoint(request: ChatModel, session: UserSession):
    async def response_stream() -> AsyncGenerator[bytes, None]:
        buffer = ""
        async for chunk in ollama_client(request.message, session):
            if chunk and 'message' in chunk and 'content' in chunk['message']:
                # Accumulate content in buffer
                buffer += chunk['message']['content']
                # If we have a complete word or punctuation, yield it
                if buffer.endswith((' ', '.', '!', '?', '\n')):
                    response_json = {
                        "content": buffer,
                        "isFinished": False
                    }
                    yield f"{json.dumps(response_json)}\n".encode('utf-8')
                    buffer = ""

        # Yield any remaining content with isFinished flag
        if buffer:
            response_json = {
                "content": buffer,
                "isFinished": True
            }
            yield f"{json.dumps(response_json)}\n".encode('utf-8')
        else:
            # Send final empty message with isFinished flag if buffer is empty
            response_json = {
                "content": "",
                "isFinished": True
            }
            yield f"{json.dumps(response_json)}\n".encode('utf-8')

    return StreamingResponse(
        response_stream(),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Transfer-Encoding": "chunked"
        }
    )

@app.post("/register")
async def add_user(user_model: UserModel, session: UserSession):
    try:
        user = users.register_user(user_model, session)
        print("data: saved", user)
        return {"message": "Registration completed successfully", "data": user}
    
    except HTTPException as e:
        print(f"HTTPException: {e}")
        raise e
    
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database operation failed. Please try again : {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

    finally:
        session.close()
        print("a")

@app.post("/login")
async def login_user(user_data: UserLoginModel, session: UserSession):
    try:
        user = auth.login(user_data, session)
        return {"message": "logged in completed successfully", "data": user}
    
    except HTTPException as e:
        print(f"HTTPException: {e}")
        raise e
    
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database operation failed. Please try again : {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.post("/register-organization")
async def register_org(user_model: ScrapModel, session: UserSession):
    try:
        org = organization.register_organization(user_model, session)
        return {"message": "Organization Registration completed successfully", "data": org}
    
    except HTTPException as e:
        print(f"HTTPException: {e}")
        raise e
    
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database operation failed. Please try again : {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

    finally:
        session.close()

@app.put("/organization/{organization_domain}", response_model=Orgnization)
async def update_organization(organization_domain: str, data: UpdateOrgnizationModel, session: UserSession):
    try:
        org = update_organization(organization_domain, data, session)
        return {"message": "Organization updated completed successfully", "data": org}
    
    except HTTPException as e:
        print(f"HTTPException: {e}")
        raise e
    
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database operation failed. Please try again : {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

    finally:
        session.close()


@app.get("/organization/{organization_domain}")
async def get_organization(organization_domain: str, session: UserSession):
    try:
        org = organization.get_organization(organization_domain, session)
        return {"message": "Organization data", "data": org}
    
    except HTTPException as e:
        print(f"HTTPException: {e}")
        raise e
    
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database operation failed. Please try again : {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

    finally:
        session.close()
