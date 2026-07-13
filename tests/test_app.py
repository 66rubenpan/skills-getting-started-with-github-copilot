import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))


client = TestClient(app)


def test_get_activities_is_not_cached():
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    remove_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    assert remove_response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_unregister_unknown_participant_returns_not_found():
    response = client.delete(
        "/activities/Chess Club/participants/ghost@mergington.edu"
    )

    assert response.status_code == 404
