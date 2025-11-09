from fastapi.testclient import TestClient
import pytest

from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Ensure known activity present
    assert "Chess Club" in data


def test_signup_and_remove_participant_cycle():
    activity = "Chess Club"
    test_email = "test_student@example.com"

    # Ensure test email not already present
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert test_email in activities[activity]["participants"]

    # Signup again should fail (student already signed up for an activity globally)
    resp2 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp2.status_code == 400

    # Remove participant
    resp3 = client.delete(f"/activities/{activity}/participants?email={test_email}")
    assert resp3.status_code == 200
    assert test_email not in activities[activity]["participants"]


def test_remove_nonexistent_participant_returns_404():
    activity = "Programming Class"
    email = "no_such_student@example.com"

    # Ensure not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 404


@pytest.fixture(autouse=True)
def restore_state():
    # After each test, ensure activities dict still has expected keys and minimal consistency
    yield
    # No-op for now; tests mutate in-memory state but clean themselves up.
