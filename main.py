from fastapi import FastAPI, Depends
from data_source.webscraper.index import WebCrawler
from db.index import create_db_and_tables, UserSession
from pydantic import BaseModel, Field, HttpUrl
from contextlib import asynccontextmanager
from db.actions.vectors import get_similar_vectors
from db.actions.web_scrapper import list_webscraps, save_webscrap

from typing import List
class ScrapModel(BaseModel):
    base_url: HttpUrl = Field(..., example="https://example.com")
    depth: int = Field(..., ge=1, le=10, example=3)
    max_pages: int = Field(..., gt=0, example=2)

class VectorQueryModel(BaseModel):
    query_vector: List[float] = Field(..., example=[0.1, 0.2, 0.3])
    top_k: int = Field(5, example=5)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

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
    save_webscrap(data, session)
    return {"message": "Crawling completed successfully"}
