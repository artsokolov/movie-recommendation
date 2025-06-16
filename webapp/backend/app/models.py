from typing import List
from pydantic import BaseModel, Field


class Review(BaseModel):
    rating: float = Field(..., ge=0, le=10)
    comment: str


class Movie(BaseModel):
    id: int
    title: str
    description: str
    reviews: List[Review]


class MovieResponse(BaseModel):
    movies: List[Movie]


class MovieRequest(BaseModel):
    description: str
