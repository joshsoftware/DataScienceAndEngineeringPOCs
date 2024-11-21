from fastapi import FastAPI, Depends
from data_source.webscraper.index import WebCrawler
from db.index import create_db_and_tables, UserSession
from pydantic import BaseModel, Field, HttpUrl
from contextlib import asynccontextmanager
from db.actions.web_scraper import save_webscrap, list_webscraps

class ScrapModel(BaseModel):
    base_url: HttpUrl = Field(..., example="https://example.com")
    depth: int = Field(..., ge=1, le=10, example=3)
    max_pages: int = Field(..., gt=0, example=2)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/web-scrap/")
async def get_webscrap(session: UserSession):
    return list_webscraps(session)

@app.post("/web-scrap/")
async def scrap_website(scrap_model: ScrapModel, session: UserSession):
    crawler = WebCrawler(str(scrap_model.base_url), depth=scrap_model.depth, max_pages=scrap_model.max_pages)
    crawler.crawl()
    data = crawler.save_results()
    save_webscrap(data, session)
    return {"message": "Crawling completed successfully"}
