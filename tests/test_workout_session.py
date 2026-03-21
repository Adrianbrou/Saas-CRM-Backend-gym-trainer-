from app.services import workout_session_service
from app.services import gym_service
from app.services import staff_service
from app.schemas.workout_session import WorkoutSessionCreate
from app.schemas.gym import GymCreate
from app.schemas.staff import StaffCreate
from app.services.workout_session_service import AttendanceCreate
import pytest
from datetime import datetime


def test_create_session(db):
    gym_data = GymCreate(name="Test Gym", location="Test location")
    gym = gym_service.register_gym(db, gym_data)
    staff_data = StaffCreate(role="manager", name="Test name", email="Test@email.com",
                             phone="234343434", gym_id=gym.id, password="1234")

    staff = staff_service.register_staff(db, staff_data)
    session_data = WorkoutSessionCreate(
        gym_id=gym.id, staff_id=staff.id, scheduled_at=datetime.now())

    session = workout_session_service.create_session(db, session_data)

    assert session.id is not None
    assert session.staff_id == staff.id
    assert session.gym_id == gym.id


def test_trainer_not_found_in_session(db):
    gym_data = GymCreate(name="Test Gym", location="Test location")
    gym = gym_service.register_gym(db, gym_data)

    session_data = WorkoutSessionCreate(
        gym_id=gym.id, staff_id=9999, scheduled_at=datetime.now())
    with pytest.raises(ValueError):
        workout_session_service.create_session(db, session_data)


def test_member_not_found_in_session(db):
    gym_data = GymCreate(name="Test Gym", location="Test location")
    gym = gym_service.register_gym(db, gym_data)
    staff_data = StaffCreate(role="manager", name="Test name", email="Test@email.com",
                             phone="234343434", gym_id=gym.id, password="1234")

    staff = staff_service.register_staff(db, staff_data)
    session_data = WorkoutSessionCreate(
        gym_id=gym.id, staff_id=staff.id, scheduled_at=datetime.now())

    session = workout_session_service.create_session(db, session_data)
    data_attendance = AttendanceCreate(
        workout_session_id=session.id, member_id=999)
    with pytest.raises(ValueError):
        workout_session_service.add_member_to_session(db, data_attendance)
