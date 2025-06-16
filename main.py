from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


class MovieRecommendationRequest(BaseModel):
    description: str = Field(min_length=50)


@app.post('/recommendation')
def recommendation_handler(req: MovieRecommendationRequest):
    """
    :param req:
    :return:
    """
    return {
        "movies": [
            {
                "title": "Matrix",
                "description": "The Matrix is a 1999 science fiction action film written and directed by the Wachowskis"
            }
        ]
    }
