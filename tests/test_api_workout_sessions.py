from datetime import datetime


def test_create_session(auth_client):
    response = auth_client.post("/workout-sessions/", json={
        "gym_id": 1,
        "staff_id": 1,
        "scheduled_at": datetime.now().isoformat()
    })
    assert response.status_code == 201
    assert response.json()["gym_id"] == 1


def test_create_session_trainer_not_found(auth_client):
    response = auth_client.post("/workout-sessions/", json={
        "gym_id": 1,
        "staff_id": 9999,
        "scheduled_at": datetime.now().isoformat()
    })
    assert response.status_code == 400


def test_add_member_to_session(auth_client):
    # create member
    member = auth_client.post("/members/", json={
        "name": "John Doe",
        "email": "john@test.com",
        "phone": "123456789",
        "gym_id": 1
    })
    member_id = member.json()["id"]

    # create session
    session = auth_client.post("/workout-sessions/", json={
        "gym_id": 1,
        "staff_id": 1,
        "scheduled_at": datetime.now().isoformat()
    })
    session_id = session.json()["id"]

    # add member to session
    response = auth_client.post(f"/workout-sessions/{session_id}/members", json={
        "workout_session_id": session_id,
        "member_id": member_id
    })
    assert response.status_code == 201


def test_remove_member_from_session(auth_client):
    # create member
    member = auth_client.post("/members/", json={
        "name": "John Doe",
        "email": "john@test.com",
        "phone": "123456789",
        "gym_id": 1
    })
    member_id = member.json()["id"]

    # create session
    session = auth_client.post("/workout-sessions/", json={
        "gym_id": 1,
        "staff_id": 1,
        "scheduled_at": datetime.now().isoformat()
    })
    session_id = session.json()["id"]

    # add then remove
    auth_client.post(f"/workout-sessions/{session_id}/members", json={
        "workout_session_id": session_id,
        "member_id": member_id
    })
    response = auth_client.delete(f"/workout-sessions/{session_id}/members/{member_id}")
    assert response.status_code == 200
