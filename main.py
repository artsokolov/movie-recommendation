import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

app = FastAPI()

OPENAI_API_KEY = ""
MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-3-small"
PROMPT_TEMPLATE = """
You are helping a user reformulate their vague movie request into a detailed, clear expression of the kind of movie they want to watch.

Your task is to rewrite the user’s request as a single, rich paragraph that describes the desired movie in detail. Do not mention any specific movies, characters, actors, or directors. Do not invent fake titles or fictional plots.

Describe the kind of movie the user is looking for by covering:

- Genre and tone
- Narrative focus or themes
- Emotional experience they want
- Pacing and atmosphere
- Type of ending they expect

Write from the user's perspective using first-person language (e.g., “I’m looking for…”). Respond only with the paragraph, no extra text, titles, or headings..
"""

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
                temperature=0.2
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
    return {"detailed": detailed, "embedding": embedding}
