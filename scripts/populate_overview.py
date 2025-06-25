import asyncio
import sqlite3
import pandas as pd
import httpx
from pathlib import Path


TMDB_TOKEN = ''
CSV_PATH = 'data/movies.csv'
DB_PATH = 'temp.db'
API_URL = 'https://api.themoviedb.org/3/find/{}?external_source=imdb_id'

HEADERS = {
    'Authorization': f'Bearer {TMDB_TOKEN}',
    'accept': 'application/json'
}

# Получаем уже существующие imdb_id
def get_existing_imdb_ids(cursor):
    cursor.execute('SELECT imdb_id FROM movies')
    return set(row[0] for row in cursor.fetchall())

# Вставка одной записи
def insert_movie(cursor, imdb_id, title, overview):
    cursor.execute('''
        INSERT INTO movies (imdb_id, title, overview)
        VALUES (?, ?, ?)
    ''', (imdb_id, title, overview))

# Асинхронный запрос к TMDb
async def fetch_overview(client, imdb_id):
    url = API_URL.format(imdb_id)
    try:
        response = await client.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            movie_results = data.get("movie_results", [])
            if movie_results:
                return imdb_id, movie_results[0].get("overview", "")
        else:
            print(f"[ERROR] {imdb_id} — HTTP {response.status_code}")
    except Exception as e:
        print(f"[EXCEPTION] {imdb_id} — {e}")
    return imdb_id, None

# Основной процесс
async def main():
    if not Path(CSV_PATH).exists():
        print(f"[ERROR] CSV not found: {CSV_PATH}")
        return

    df = pd.read_csv(CSV_PATH, usecols=['tconst', 'primaryTitle'])
    print(f"[INFO] Loaded {len(df)} records from CSV")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        existing_ids = get_existing_imdb_ids(cursor)
        records = df[~df['tconst'].isin(existing_ids)].to_dict(orient='records')
        total = len(records)
        print(f"[INFO] {total} new movies to process")

        i = 0
        async with httpx.AsyncClient() as client:
            while i < total:
                batch = records[i:i+40]

                # Асинхронно отправляем все запросы
                tasks = [
                    fetch_overview(client, row['tconst']) for row in batch
                ]
                results = await asyncio.gather(*tasks)

                for idx, (imdb_id, overview) in enumerate(results):
                    if overview:
                        title = batch[idx]['primaryTitle']
                        insert_movie(cursor, imdb_id, title, overview)
                        print(f"[INSERTED] {title} ({imdb_id})")
                    else:
                        print(f"[SKIPPED] {imdb_id} — no overview")

                conn.commit()
                i += 40

                if i < total:
                    print(f"[WAITING] Sleeping 10s... Processed {i}/{total}")
                    await asyncio.sleep(10)

        print(f"[DONE] Processed {i} movies")

# Точка входа
if __name__ == "__main__":
    asyncio.run(main())