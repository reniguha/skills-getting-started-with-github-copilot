def test_get_activities_returns_activity_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    json_data = response.json()
    assert "Chess Club" in json_data
    assert "Programming Class" in json_data
    assert isinstance(json_data["Chess Club"]["participants"], list)


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_signup_for_activity_successful(client):
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activities_response = client.get("/activities").json()
    assert email in activities_response[activity_name]["participants"]


def test_signup_for_activity_duplicate_fails(client):
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for an activity"


def test_signup_for_activity_not_found(client):
    response = client.post("/activities/Unknown/signup", params={"email": "someone@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_successful(client):
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}

    activities_response = client.get("/activities").json()
    assert email not in activities_response[activity_name]["participants"]


def test_unregister_from_activity_activity_not_found(client):
    response = client.delete("/activities/Unknown/participants", params={"email": "someone@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_participant_not_found(client):
    response = client.delete("/activities/Chess Club/participants", params={"email": "absent@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
