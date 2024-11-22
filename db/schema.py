# id, -- Unique identifier for each entry
# websiteUrl , -- URL of the website (max length for URLs)
# websiteDepth , -- Depth of the website
# websiteMaxNumberOfPages, -- Max number of pages to scrape
# lastScrapedDate , -- Last time the website was scraped
# filePath -- Path to where data is stored

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, JSON
from typing import Any
from pgvector.sqlalchemy import Vector

class ScrapData(SQLModel, table=True):
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    websiteUrl: str = Field(sa_column=Column(String(255)))
    websiteDepth: int
    websiteMaxNumberOfPages: int
    lastScrapedDate: str
    filePath: str
class VectorData(SQLModel, table=True):
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    metaData: dict = Field(sa_column=Column(JSON))
    embedding: Any = Field(sa_column=Column(Vector(3)))