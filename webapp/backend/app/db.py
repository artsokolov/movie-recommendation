import random

from app.models import Movie, Review


class MovieNotFoundError(Exception):
    pass


# Mock database for testing purposes
MOCK_MOVIES: list[Movie] = [
    Movie(
        id=1,
        title="Inception",
        description="A skilled thief leads a team into dreams to steal secrets.",
        reviews=[
            Review(rating=9.0, comment="Mind-blowing!"),
            Review(rating=8.5, comment="Brilliant but complex."),
        ],
    ),
    Movie(
        id=2,
        title="The Matrix",
        description=(
            "A hacker discovers the true nature of reality and fights machines."
        ),
        reviews=[
            Review(rating=9.5, comment="A classic."),
        ],
    ),
    Movie(
        id=3,
        title="Interstellar",
        description="A team travels through a wormhole to save humanity.",
        reviews=[
            Review(rating=8.8, comment="Visually stunning and emotional."),
            Review(rating=9.2, comment="A masterpiece."),
        ],
    ),
    Movie(
        id=4,
        title="The Godfather",
        description=(
            "The aging patriarch of an organized crime dynasty transfers control"
            "to his reluctant son."
        ),
        reviews=[
            Review(rating=9.2, comment="An epic tale of family and power."),
            Review(rating=9.0, comment="One of the greatest films of all time."),
            Review(rating=9.5, comment="Timeless classic."),
        ],
    ),
    # bad movies
    Movie(
        id=5,
        title="The Room",
        description="A melodramatic story of love and betrayal.",
        reviews=[
            Review(rating=3.0, comment="So bad it's good."),
        ],
    ),
    Movie(
        id=6,
        title="Birdemic",
        description="A love story interrupted by an attack of mutant birds.",
        reviews=[
            Review(rating=2.0, comment="Terrible special effects."),
            Review(rating=1.5, comment="Unintentionally hilarious."),
        ],
    ),
    Movie(
        id=7,
        title="Plan 9 from Outer Space",
        description="Aliens resurrect the dead to conquer Earth.",
        reviews=[],
    ),
]


class MockDB:
    def get_movies_by_description(
        self, description: str, limit: int = 3
    ) -> list[Movie]:
        """Mock method to simulate fetching movies from a database based on
        description. This method randomly selects movies with limited results
        to simulate a database query.

        Args:
            description (str): The description to filter movies by.
            limit (int): The maximum number of movies to return.

        Returns:
            List[Movie]: A list of movies that match the description.
        """

        selected_movies = random.sample(MOCK_MOVIES, min(limit, len(MOCK_MOVIES)))
        return selected_movies

    def get_movie_by_id(self, movie_id: int) -> Movie:
        """Mock method to simulate fetching a movie by its ID.

        Args:
            movie_id (int): The ID of the movie to fetch.

        Returns:
            Movie: The movie with the specified ID.

        Raises:
            MovieNotFoundError: If no movie with the given ID is found.
        """

        for movie in MOCK_MOVIES:
            if movie.id == movie_id:
                return movie

        raise MovieNotFoundError(f"Movie with ID {movie_id} not found.")

    def get_reviews_by_movie_id(self, movie_id: int) -> list[Review]:
        """Mock method to simulate fetching reviews for a movie by its ID.

        Args:
            movie_id (int): The ID of the movie to fetch reviews for.

        Returns:
            List[Review]: A list of reviews for the specified movie, or an empty
            list if not found.
        """

        movie: Movie = self.get_movie_by_id(movie_id)
        reviews: list[Review] = (
            movie.reviews
        )  # mypy cannot infer type here, manually specify it
        return reviews

    def get_all_movies(self) -> list[Movie]:
        """Mock method to simulate fetching all movies from the database.

        Returns:
            List[Movie]: A list of all movies.
        """

        return MOCK_MOVIES

    def get_movies_limit(self, limit: int = 3) -> list[Movie]:
        """Mock method to simulate fetching a limited number of movies from the
        database.

        Args:
            limit (int): The maximum number of movies to return.

        Returns:
            List[Movie]: A list of movies limited to the specified count.
        """

        return MOCK_MOVIES[:limit]


# Instantiate singleton mock DB connection
mock_db: MockDB = MockDB()
