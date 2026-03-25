import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # (No special setup needed, using default app state)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_duplicate_returns_400():
    # Arrange - sign up a student once successfully
    client.post("/activities/Chess Club/signup?email=duplicate_test@mergington.edu")

    # Act - attempt to sign up the same student again
    response = client.post("/activities/Chess Club/signup?email=duplicate_test@mergington.edu")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_removes_participant():
    # Arrange - sign up a student so they can be removed
    client.post("/activities/Chess Club/signup?email=unregister_test@mergington.edu")

    # Act
    response = client.post("/activities/Chess Club/unregister?email=unregister_test@mergington.edu")

    # Assert
    assert response.status_code == 200
    activities_response = client.get("/activities")
    assert "unregister_test@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]


def test_unregister_unregistered_returns_400():
    # Arrange - email that was never signed up
    email = "never_registered@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess Club/unregister?email={email}")

    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
