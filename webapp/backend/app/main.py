from fastapi import FastAPI
from app.routers import movies

app = FastAPI(title="Movie Recommendation API")

app.include_router(movies.router)
