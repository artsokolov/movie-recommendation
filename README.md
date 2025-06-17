# 🎬 Movie Recommendation

**Movie Recommendation** is a full-stack application that provides intelligent movie suggestions based on a user's free-form textual input. Instead of relying on predefined genres or filters, users can simply describe the kind of movie they're in the mood for — for example, "something like The Matrix but with a romantic plotline" — and the system will return relevant and tailored recommendations.

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

# Backend API

```bash
git clone https://github.com/artsokolov/movie-recommendation
cd movie-recommendation/webapp/backend
uv pip install -r pyproject.toml
uv run main:app --reload
```

