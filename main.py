import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient, models

app = FastAPI()

OPENAI_API_KEY = ""
MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-3-small"
PROMPT_TEMPLATE = """
You are transforming a vague user request for a movie into a precise, detailed description of the kind of film they are looking for.

Your goal is to generate one rich paragraph that describes the ideal movie using objective and analytical language. Do not mention any specific movie titles, characters, actors, or directors. Do not invent new fictional movies. Focus on abstract qualities only.

Be as clear and specific as possible about:

- Genre and subgenre (e.g., high-concept science fiction, psychological drama)
- Tone and mood (e.g., dark, cerebral, tense, immersive)
- Core themes (e.g., consciousness, reality, identity, free will)
- Narrative structure (e.g., nonlinear, slow-burn, twist-driven)
- Emotional impact (e.g., unsettling, thought-provoking, introspective)
- Style of ending (e.g., ambiguous, philosophical, open to interpretation)

Avoid hedging language like “possibly” or “likely.” Use confident, descriptive phrases.

Output only the paragraph — no titles, summaries, or extra text.
"""
QDRANT_URL = "http://quadrant:6333"
COLLECTION_NAME = "movies"

class OpenAIRecommender:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def description_to_detailed(self, description: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": PROMPT_TEMPLATE},
                    {"role": "user", "content": description}
                ],
                max_tokens=700,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API error (chat): {str(e)}")

    async def description_to_embedding(self, detailed_description: str) -> list:
        try:
            response = await self.client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=detailed_description
            )
            return response.data[0].embedding
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API error (embedding): {str(e)}")

recommender = OpenAIRecommender(api_key=OPENAI_API_KEY)

class MovieRecommendationRequest(BaseModel):
    description: str = Field(min_length=50)

@app.post('/recommendation')
async def recommendation_handler(req: MovieRecommendationRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not set")

    detailed = await recommender.description_to_detailed(req.description)

    embedding = await recommender.description_to_embedding(detailed)

    qdrant = AsyncQdrantClient(url=QDRANT_URL)
    search_result = await qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=5
    )

    movies = []
    for hit in search_result:
        payload = hit.payload or {}
        movies.append({
            "imdb_id": payload.get("imdb_id"),
            "plot": payload.get("plot")
        })
    await qdrant.close()
    return {"description": detailed, "movies": movies}
