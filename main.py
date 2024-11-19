from fastapi import FastAPI, Depends
from data_source.webscraper.index import WebCrawler
from db.index import create_db_and_tables, UserSession
from pydantic import BaseModel, Field, HttpUrl
from db.actions.web_scraper import save_webscrap , list_webscraps

app = FastAPI()

class ScrapModel(BaseModel):
    base_url: HttpUrl = Field(..., example="https://example.com")
    depth: int = Field(..., ge=1, le=10, example=3)
    max_pages: int = Field(..., gt=0, example=2)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
@app.get("/web-scrap/")
def get_webscrap(session: UserSession):
    return list_webscraps(session)

@app.post("/web-scrap/")
def scrap_website(scrap_model: ScrapModel, session: UserSession):
    crawler = WebCrawler(str(scrap_model.base_url), depth=scrap_model.depth, max_pages=scrap_model.max_pages)
    crawler.crawl()
    data = crawler.save_results()
    save_webscrap(data, session)
    return {"message": "Crawling completed successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)