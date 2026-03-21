from app.services import workout_service
from app.schemas.workout import WorkoutCreate
from app.models.workout import BodyPart

import pytest


def test_create_workout(db):
    body_part = BodyPart(name="Chest")
    db.add(body_part)

    db.commit()
    db.refresh(body_part)
    data = WorkoutCreate(name="Test workout name", body_part_id=body_part.id)

    workout = workout_service.create_workout(db, data)

    assert workout.id is not None
    assert workout.body_part == body_part
    assert workout.body_part_id == body_part.id


def test_duplicate_workout(db):
    body_part = BodyPart(name="Chest")
    db.add(body_part)

    db.commit()
    db.refresh(body_part)
    data = WorkoutCreate(name="Test workout name", body_part_id=body_part.id)

    workout_service.create_workout(db, data)
    with pytest.raises(ValueError):
        workout_service.create_workout(db, data)


def test_workout_not_found(db):
    with pytest.raises(ValueError):
        workout_service.get_workout(db, 999)
