from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # No setup needed for in-memory activities
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()

def test_signup_success():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

def test_signup_activity_not_found():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["error"] == "Activity not found"

def test_unregister_success():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"

def test_unregister_not_signed_up():
    # Arrange
    email = "not_signed_up@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert response.json()["error"] == "Student not signed up"

def test_unregister_activity_not_found():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["error"] == "Activity not found"
