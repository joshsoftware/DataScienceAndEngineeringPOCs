# id, -- Unique identifier for each entry
# websiteUrl , -- URL of the website (max length for URLs)
# websiteDepth , -- Depth of the website
# websiteMaxNumberOfPages, -- Max number of pages to scrape
# lastScrapedDate , -- Last time the website was scraped
# filePath -- Path to where data is stored

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String

class ScrapData(SQLModel, table=True):
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    websiteUrl: str = Field(sa_column=Column(String(255)))
    websiteDepth: int
    websiteMaxNumberOfPages: int
    lastScrapedDate: str
    filePath: str