import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import asyncio
import sqlite3
from typing import Tuple

from ai import Converter
from db import Database

import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = 'temp.db'
QDRANT_HOST = os.getenv('QDRANT_HOST', 'quadrant')
QDRANT_PORT = int(os.getenv('QDRANT_PORT', 6333))
OPENAI_API_KEY = ''


CONCURRENCY_LIMIT = 5


def get_unhandled_movies(cursor) -> list[Tuple[int, str, str, str]]:
    cursor.execute('''
        SELECT id, imdb_id, title, overview
        FROM movies
        WHERE handled = 0
    ''')
    return cursor.fetchall()


def update_movie(cursor, movie_id: int, detailed_description: str):
    cursor.execute('''
        UPDATE movies
        SET detailed_description = ?, handled = 1
        WHERE id = ?
    ''', (detailed_description, movie_id))


# Обработка одного фильма
async def process_movie(semaphore: asyncio.Semaphore, movie: Tuple[int, str, str, str], converter: Converter, db: Database):
    movie_id, imdb_id, title, overview = movie

    async with semaphore:
        try:
            print(f"[START] {title} ({imdb_id})")

            detailed = await converter.movie_overview_detailed(overview)

            embedding = await converter.embedding(detailed)

            db.insert(
                vec=embedding,
                payload={
                    'title': title,
                    'imdb_id': imdb_id,
                    'overview': overview
                }
            )

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            update_movie(cursor, movie_id, detailed)
            conn.commit()
            conn.close()

            print(f"[OK] {title} обработан")

        except Exception as e:
            print(f"[ERROR] {title} ({imdb_id}): {e}")


async def main():
    converter = Converter(api_key=OPENAI_API_KEY)
    db = Database(host=QDRANT_HOST, port=QDRANT_PORT)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    movies = get_unhandled_movies(cursor)
    conn.close()

    print(f"[INFO] Найдено {len(movies)} фильмов для обработки")

    if not movies:
        return

    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    tasks = [
        process_movie(semaphore, movie, converter, db)
        for movie in movies
    ]

    await asyncio.gather(*tasks)
    print("[DONE] Все фильмы обработаны")


if __name__ == "__main__":
    asyncio.run(main())
