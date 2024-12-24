from pydantic import BaseModel, Field

class ScrapModel(BaseModel):
    url: str = Field(..., example="https://example.com")
    domain: str = Field(..., example="https://example.com")
    depth: int = Field(..., ge=1, le=10, example=3)
    max_pages: int = Field(..., gt=0, example=2)
    frequency: int = Field(..., gt=0, example=2)
    user: int = Field(..., example=2)
    