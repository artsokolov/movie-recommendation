import asyncio
import sqlite3
import uuid
from qdrant_client import AsyncQdrantClient, models
from main import OpenAIRecommender, OPENAI_API_KEY, EMBEDDING_MODEL

QDRANT_URL = "http://quadrant:6333"
COLLECTION_NAME = "movies"
VECTOR_SIZE = 1536  # для text-embedding-3-small

async def main():
    # 1. Подключение к Qdrant
    qdrant = AsyncQdrantClient(url=QDRANT_URL)
    # 2. Проверка/создание коллекции
    exists = await qdrant.collection_exists(COLLECTION_NAME)
    if not exists:
        await qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )
    # 3. Подключение к SQLite
    conn = sqlite3.connect("movies.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT imdb_id, plot FROM movies WHERE plot IS NOT NULL AND handled = 0")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} movies to process.")
    # 4. Инициализация OpenAIRecommender
    recommender = OpenAIRecommender(api_key=OPENAI_API_KEY)
    # 5. Обработка
    for row in rows:
        imdb_id = row["imdb_id"]
        plot = row["plot"]
        try:
            embedding = await recommender.description_to_embedding(plot)
            # Генерируем UUID для id точки
            point_id = str(uuid.uuid4())
            await qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload={"imdb_id": imdb_id, "plot": plot}
                    )
                ]
            )
            # Обновляем handled в SQLite
            cursor.execute("UPDATE movies SET handled = 1 WHERE imdb_id = ?", (imdb_id,))
            conn.commit()
            print(f"Processed {imdb_id}")
        except Exception as e:
            print(f"Error processing {imdb_id}: {e}")
    conn.close()
    await qdrant.close()

if __name__ == "__main__":
    asyncio.run(main()) 