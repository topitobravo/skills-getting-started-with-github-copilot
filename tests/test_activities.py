"""Tests for activities endpoints using AAA (Arrange-Act-Assert) pattern."""


def test_get_activities(client):
    # Arrange: none (use default state)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    email = "test@student.edu"

    # Act
    resp = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert f"Signed up {email}" in resp.json().get("message", "")

    # Verify participant appears in activity
    resp2 = client.get("/activities")
    assert email in resp2.json()["Chess Club"]["participants"]


def test_signup_duplicate(client):
    # Arrange: use an email already present in the initial data
    email = "michael@mergington.edu"

    # Act
    resp = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert resp.status_code == 400


def test_unregister_success(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    resp = client.delete("/activities/Chess Club/unregister", params={"email": email})

    # Assert
    assert resp.status_code == 200

    # Verify participant no longer appears
    resp2 = client.get("/activities")
    assert email not in resp2.json()["Chess Club"]["participants"]


def test_unregister_not_signed(client):
    # Arrange
    email = "not-signed@student.edu"

    # Act
    resp = client.delete("/activities/Chess Club/unregister", params={"email": email})

    # Assert
    assert resp.status_code == 400
