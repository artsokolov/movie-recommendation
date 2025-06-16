import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_get_all_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_movies_limit():
    response = client.get("/movies/limit/2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_get_movie_by_id_success():
    response = client.get("/movies/1")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert data["id"] == 1

def test_get_movie_by_id_not_found():
    response = client.get("/movies/9999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Movie with ID 9999 not found."

def test_get_reviews_by_movie_id_success():
    response = client.get("/movies/1/reviews")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_reviews_by_movie_id_not_found():
    response = client.get("/movies/9999/reviews")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Movie with ID 9999 not found."


def test_get_movies_recommendation():
    response = client.post("/movies/recommend", json={"description": "A great action movie"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0