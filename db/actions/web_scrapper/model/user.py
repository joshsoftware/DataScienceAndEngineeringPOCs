from pydantic import BaseModel, Field


class UserModel(BaseModel):
    name: str = Field(..., example="dummy name")
    email: str = Field(..., example="example@example.com")
    domain: str = Field(..., example="example.com")
    contactNumber: str = Field(..., min_length=5, max_length=15, example="+1234567890")
    password: str = Field(..., example="password123")


class UserLoginModel(BaseModel):
    email: str = Field(..., example="example@example.com")
    password: str = Field(..., example="password123")

class ScrapModel(BaseModel):
    url: str = Field(..., example="https://example.com")
    domain: str = Field(..., example="https://example.com")
    depth: int = Field(..., ge=1, le=10, example=3)
    max_pages: int = Field(..., gt=0, example=2)
    frequency: int = Field(..., gt=0, example=2)
    user: int = Field(..., example=2)
    