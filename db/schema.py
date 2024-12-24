# id, -- Unique identifier for each entry
# websiteUrl , -- URL of the website (max length for URLs)
# websiteDepth , -- Depth of the website
# websiteMaxNumberOfPages, -- Max number of pages to scrape
# lastScrapedDate , -- Last time the website was scraped
# filePath -- Path to where data is stored

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, JSON, Boolean, Text
from typing import Any
from pgvector.sqlalchemy import Vector

class UserDetails(SQLModel, table=True):
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column(String(255), nullable=False))
    email: str = Field(sa_column=Column(String(255), nullable=False, unique=True))
    domain: str = Field(sa_column=Column(String(255), nullable=False))
    contact_number: str = Field(sa_column=Column(String(15), nullable=False))
    hashed_password: str = Field(sa_column=Column(Text, nullable=False))
    email_confirmed: bool = Field(default=False, sa_column=Column(Boolean, default=False))
    deleted_user: bool = Field(default=False, sa_column=Column(Boolean, default=False))

class Orgnization(SQLModel, table=True):
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    websiteUrl: str = Field(sa_column=Column(String(255),nullable=False, unique=True))
    websiteDomain: str = Field(sa_column=Column(String(255), nullable=False, unique=True))
    websiteMaxNumberOfPages: int = Field(default=None, sa_column=Column(Integer))
    websiteDepth: int = Field(default=None, sa_column=Column(Integer))
    websiteFrequency: int = Field(default=None, sa_column=Column(Integer))
    filePath: str = Field(default="", sa_column=Column(String(255), default=""))
    lastScrapedDate: str = Field(default="", sa_column=Column(String(255), default=""))
    user_id: int = Field(default=None, foreign_key="userdetails.id")


class OrgDataEmbedding(SQLModel, table=True):
    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    metaData: dict = Field(sa_column=Column(JSON))
    #embedding: Any = Field(sa_column=Column(Vector(1024)))
    org_id: int = Field(default=None, foreign_key="orgnization.id")