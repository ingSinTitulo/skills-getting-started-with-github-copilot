from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_get_activities_returns_activity_catalog():
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["schedule"]
    assert isinstance(payload["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant():
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    original_participants = deepcopy(activities[activity_name]["participants"])

    try:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    original_participants = deepcopy(activities[activity_name]["participants"])

    try:
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Removed {email} from {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants
