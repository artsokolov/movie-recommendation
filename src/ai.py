from openai import AsyncOpenAI
from prompts import MOVIE_DETAILED_PROMPT, USER_DESCRIPTION_PROMPT

COMPLETION_MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-3-small"

class Converter:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def _request_completion(self, prompt: str, content: str) -> str:
        response = await self.client.chat.completions.create(
            model=COMPLETION_MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ],
            max_tokens=700,
            temperature=0.1
        )

        return response.choices[0].message.content

    async def movie_overview_detailed(self, overview: str):
        return await self._request_completion(MOVIE_DETAILED_PROMPT, overview)

    async def user_description_detailed(self, description: str):
        return await self._request_completion(USER_DESCRIPTION_PROMPT, description)

    async def embedding(self, content: str) -> list:
        response = await self.client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=content
        )

        return response.data[0].embedding