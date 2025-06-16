from typing import List
from pydantic import BaseModel, Field


class Review(BaseModel):
    rating: float = Field(..., ge=0, le=10)
    comment: str


class Movie(BaseModel):
    id: int
    title: str
    description: str = Field(..., max_length=200)
    reviews: List[Review]

class MovieRequest(BaseModel):
    description: str = Field(..., max_length=100)