import os
import requests
import sqlite3
import polars as pl
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")


def load_data(source: str, debug: bool = False) -> pl.DataFrame:
    """
    Load the Parquet file into a Polars DataFrame.
    """
    # Load the Parquet file into a Polars DataFrame
    df = pl.read_parquet(source)

    if debug:
        # Print the first few rows of the DataFrame for debugging
        print(df.head(5))
        print()

    return df


def fetch_movie_data(
    tconst: str, api_key: str, full: bool = False, debug: bool = False
) -> str:
    """
    Fetch the movie plot from the OMDb API using the tconst identifier.
    """
    url = f"http://www.omdbapi.com/?i={tconst}&apikey={api_key}&plot=full"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(
            f"Error fetching data from OMDb API: {response.status_code} - {response.text}"
        )

    data = response.json()

    if debug:
        print(f"Response from OMDb API: {data}")

    if "Error" in data:
        raise Exception(f"OMDb API error: {data['Error']}")

    return data


def create_database(db_path: str = "movies.db"):
    """
    Create a SQLite database and a table for storing movie data.
    """
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS movies (
                imdb_id TEXT PRIMARY KEY,
                title TEXT,
                original_title TEXT,
                year INTEGER,
                runtime INTEGER,
                genre TEXT,
                plot TEXT,
                language TEXT,
                country TEXT,
                director TEXT,
                actors TEXT,
                poster_url TEXT,
                imdb_rating REAL,
                imdb_votes INTEGER
            )
            """
        )

def save_movie_to_db(movie: dict, db_path: str = "movies.db", debug: bool = False):
    """
    Save the fetched movie data to a sqlite database.
    This function only saves tconst,
    """
    movie_data = fetch_movie_data(movie["tconst"], OMDB_API_KEY, full=True, debug=debug)
    if debug:
        print(f"Fetched movie data: {movie_data}")

    def parse_runtime(runtime_str: str) -> int:
        """
        Parse the runtime string and return the runtime in minutes.
        """
        if not runtime_str:
            return 0

        if "N/A" in runtime_str or "min" not in runtime_str:
            return 0

        # Extract digits from the runtime string
        runtime_match = re.search(r"(\d+)\s*min", runtime_str)
        if runtime_match:
            return int(runtime_match.group(1))

        return 0

    import re

    def parse_str_to_int(value: str) -> int:
        if value is None:
            return None
        value = value.strip()

        if value == "" or value.upper() == "N/A":
            return None

        digits_only = re.sub(r"\D", "", value)
        if digits_only == "":
            return None
        
        return int(digits_only)
    
    def parse_str_to_float(value: str) -> float:
        if value is None:
            return None
        value = value.strip()

        if value == "" or value.upper() == "N/A":
            return None

        try:
            return float(value)
        except ValueError:
            return None
        
    def parse_str(value: str) -> str:
        if value is None:
            return None
        value = value.strip()

        if value == "" or value.upper() == "N/A":
            return None

        return value
        

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO movies (
                    imdb_id, title, original_title, year, runtime, genre,
                    plot, language, country, director, actors, poster_url,
                    imdb_rating, imdb_votes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    parse_str(movie_data.get("imdbID")),
                    parse_str(movie.get("primaryTitle")),
                    parse_str(movie.get("originalTitle")),
                    parse_str(movie_data.get("Year")),
                    parse_str_to_int(movie_data.get("Runtime")),
                    parse_str(movie_data.get("Genre")),
                    parse_str(movie_data.get("Plot")),
                    parse_str(movie_data.get("Language")),
                    parse_str(movie_data.get("Country")),
                    parse_str(movie_data.get("Director")),
                    parse_str(movie_data.get("Actors")),
                    parse_str(movie_data.get("Poster")),
                    parse_str_to_float(movie_data.get("imdbRating")),
                    parse_str_to_int(movie_data.get("imdbVotes"))
                ),
            )

            if debug:
                print(f"Movie {movie_data.get('Title')} saved to database.\n")

    except sqlite3.Error as e:
        print(f"An error occurred while saving movie data: {e}")


if __name__ == "__main__":
    df = load_data("data/title_basics_extracted.parquet", debug=True)

    create_database(db_path="movies.db")

    # select 100 random movies and save them to the database
    random_movies = df.sample(n=100).to_dicts()

    failed_movies = []

    def process_movie(movie: dict):
        """
        Process a single movie by fetching its data and saving it to the database.
        """
        try:
            save_movie_to_db(movie, db_path="movies.db", debug=True)
        except Exception as e:
            print(f"Error saving movie {movie['tconst']}: {e}")
            failed_movies.append(movie)

    with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers as needed
        futures = [executor.submit(process_movie, movie) for movie in random_movies]
        for future in as_completed(futures):
            pass

    if failed_movies:
        print(f"Failed to save {len(failed_movies)} movies:")
        for movie in failed_movies:
            print(movie)
    else:
        print("All movies saved successfully.")
        
    print("Database creation and movie data fetching completed.")