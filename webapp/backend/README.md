# 🎬 Movie Recommendation API

**Movie Recommendation API** is a FastAPI-based service that provides intelligent movie recommendations based on a free-form textual description provided by the user. Just describe the kind of movie you're in the mood for — for example, *"something like The Matrix but with a romantic plotline"* — and the API will suggest relevant films.

## 🚀 Features

- 🔍 Accepts natural language descriptions from users
- 🧠 Uses NLP models (LLMs + Embeddings) to interpret intent
- 🎥 Returns a list of movies that closely match the description
- 📦 RESTful API ready for frontend integration or external services

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — modern, fast web framework for Python
- [Pydantic](https://docs.pydantic.dev/) — for data validation
- [Uvicorn](https://www.uvicorn.org/) — ASGI server

## 📦 Installation

```bash
git clone https://github.com/artsokolov/movie-recommendation
cd movie-recommendation
uv pip install -r pyproject.toml
