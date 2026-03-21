from app.services import workout_session_service
from app.services import member_service
from app.services import gym_service
from app.services import staff_service
from app.services import progress_service
from app.services import workout_service

from app.schemas.workout_session import WorkoutSessionCreate
from app.schemas.progress import ProgressCreate
from app.schemas.member import MemberCreate
from app.schemas.workout import WorkoutCreate
from app.schemas.gym import GymCreate
from app.schemas.staff import StaffCreate
from app.models.workout import BodyPart

import pytest
from datetime import datetime


def test_log_progress(db):
    data = GymCreate(name="Test Gym", location="Test City")
    gym = gym_service.register_gym(db, data)

    member_data = MemberCreate(
        gym_id=gym.id, name="mark", email="mark@gmail.com", phone="5434356")
    member = member_service.register_member(db, member_data)

    staff_data = StaffCreate(role="manager", name="Test name", email="Test@email.com",
                             phone="234343434", gym_id=gym.id, password="1234")

    staff = staff_service.register_staff(db, staff_data)

    body_part = BodyPart(name="Chest")
    db.add(body_part)

    db.commit()
    db.refresh(body_part)

    workout_data = WorkoutCreate(name="Hyper", body_part_id=body_part.id)
    workout = workout_service.create_workout(db, workout_data)

    workout_session_data = WorkoutSessionCreate(
        gym_id=gym.id, staff_id=staff.id, scheduled_at=datetime.now())
    workout_session = workout_session_service.create_session(
        db, workout_session_data)

    progress_data = ProgressCreate(member_id=member.id, workout_id=workout.id,
                                   workout_session_id=workout_session.id, weight_kg=56, sets=3, reps=10)

    progress = progress_service.log_progress(db, progress_data)
    assert progress.id is not None
    assert progress.member_id == member.id
    assert progress.reps == progress_data.reps


def test_get_progress_by_workout_empty(db):
    result = progress_service.get_progress_by_workout(db, 9999)
    assert result == []


def test_update_progress_not_found(db):
    with pytest.raises(ValueError):
        progress_service.update_progress(db, 9999, {})


def test_progress_not_found(db):
    with pytest.raises(ValueError):
        progress_service.get_progress(db, 99)
