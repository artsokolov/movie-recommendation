import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_recommendation_valid_request():
    response = client.post("/recommendation", json={
        "description": "A dystopian future where humanity is unknowingly trapped inside a simulated reality."
    })
    assert response.status_code == 200
    json_data = response.json()
    assert "movies" in json_data
    assert isinstance(json_data["movies"], list)


def test_recommendation_invalid_request():
    response = client.post("/recommendation", json={
        "description": "Too short"
    })
    assert response.status_code == 422
    json_data = response.json()
    assert json_data["detail"][0]["loc"] == ["body", "description"]
    assert json_data["detail"][0]["type"] == "string_too_short"
