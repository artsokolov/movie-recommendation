from fastapi import APIRouter, HTTPException
from app.models import Movie, Review, RecommendationRequest
from app.db import mock_db

router = APIRouter()

@router.get("/movies", response_model=list[Movie])
async def get_all_movies() -> list[Movie]:
    """
    Fetch all movies from the database.
    
    Returns:
        List[Movie]: A list of all movies.
    """
    return mock_db.get_all_movies()

@router.get("/movies/limit/{limit}", response_model=list[Movie])
async def get_movies_limit(limit: int = 3) -> list[Movie]:
    """
    Fetch a limited number of movies from the database.
    
    Args:
        limit (int): The maximum number of movies to return. Default is 3.
    
    Returns:
        List[Movie]: A list of movies limited to the specified count.
    """
    return mock_db.get_movies_limit(limit)

@router.get("/movies/{movie_id}", response_model=Movie)
async def get_movie_by_id(movie_id: int) -> Movie:
    """
    Fetch a movie by its ID.
    
    Args:
        movie_id (int): The ID of the movie to fetch.
    
    Returns:
        Movie: The movie with the specified ID, or raises a 404 error if not found.
    """
    try:
        movie = mock_db.get_movie_by_id(movie_id)
        return movie
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/movies/{movie_id}/reviews", response_model=list[Review])
async def get_reviews_by_movie_id(movie_id: int) -> list[Review]:
    """
    Fetch reviews for a movie by its ID.
    
    Args:
        movie_id (int): The ID of the movie to fetch reviews for.
    
    Returns:
        List[Review]: A list of reviews for the specified movie, or an empty list if not found.
    """
    try:
        reviews = mock_db.get_reviews_by_movie_id(movie_id)
        return reviews
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/movies/recommend", response_model=list[Movie])
async def recommend_movies(request: RecommendationRequest) -> list[Movie]:
    """
    Recommend movies based on a description.
    
    Args:
        request (RecommendationRequest): The request containing the description for recommendations.
    
    Returns:
        List[Movie]: A list of recommended movies based on the provided description.
    """

    return mock_db.get_movies_by_description(request.description, limit=3)