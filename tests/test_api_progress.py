from datetime import datetime
from app.models.workout import BodyPart
from tests.conftest import TestingSessionLocal


def _seed_body_part(name="Chest"):
    db = TestingSessionLocal()
    body_part = BodyPart(name=name)
    db.add(body_part)
    db.commit()
    db.refresh(body_part)
    db.close()
    return body_part.id


def _setup_progress(auth_client):
    """Helper — creates all required objects and returns progress response."""
    body_part_id = _seed_body_part()

    workout = auth_client.post("/workouts/", json={
        "name": "Bench Press",
        "body_part_id": body_part_id
    })
    workout_id = workout.json()["id"]

    member = auth_client.post("/members/", json={
        "name": "John Doe",
        "email": "john@test.com",
        "phone": "123456789",
        "gym_id": 1
    })
    member_id = member.json()["id"]

    session = auth_client.post("/workout-sessions/", json={
        "gym_id": 1,
        "staff_id": 1,
        "scheduled_at": datetime.now().isoformat()
    })
    session_id = session.json()["id"]

    return auth_client.post("/progress/", json={
        "member_id": member_id,
        "workout_id": workout_id,
        "workout_session_id": session_id,
        "weight_kg": 80,
        "sets": 3,
        "reps": 10
    })


def test_log_progress(auth_client):
    response = _setup_progress(auth_client)
    assert response.status_code == 201
    assert response.json()["weight_kg"] == 80


def test_get_progress(auth_client):
    created = _setup_progress(auth_client)
    progress_id = created.json()["id"]
    response = auth_client.get(f"/progress/{progress_id}")
    assert response.status_code == 200
    assert response.json()["id"] == progress_id


def test_get_progress_not_found(auth_client):
    response = auth_client.get("/progress/9999")
    assert response.status_code == 404


def test_update_progress(auth_client):
    created = _setup_progress(auth_client)
    progress_id = created.json()["id"]
    response = auth_client.patch(f"/progress/{progress_id}", json={"reps": 12})
    assert response.status_code == 200
    assert response.json()["reps"] == 12


def test_delete_progress(auth_client):
    created = _setup_progress(auth_client)
    progress_id = created.json()["id"]
    response = auth_client.delete(f"/progress/{progress_id}")
    assert response.status_code == 200
