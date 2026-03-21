from app.services import staff_service
from app.schemas.staff import StaffCreate
from app.schemas.gym import GymCreate
from app.services import gym_service
from app.core import security


import pytest


def test_register_staff(db):
    gym_data = GymCreate(name="Test Gym", location="Test location")
    gym = gym_service.register_gym(db, gym_data)
    staff_data = StaffCreate(role="manager", name="Test name", email="Test@email.com",
                             phone="234343434", gym_id=gym.id, password="1234")

    staff = staff_service.register_staff(db, staff_data)

    assert staff.id is not None
    assert security.verify_password("1234", staff.hashed_password)
    assert staff.gym_id == gym.id


def test_duplicate_staff(db):
    gym_data = GymCreate(name="Test Gym", location="Test location")
    gym = gym_service.register_gym(db, gym_data)
    staff_data = StaffCreate(role="manager", name="Test name", email="Test@email.com",
                             phone="234343434", gym_id=gym.id, password="1234")

    staff_service.register_staff(db, staff_data)
    with pytest.raises(ValueError):
        staff_service.register_staff(db, staff_data)


def test_staff_not_found(db):
    with pytest.raises(ValueError):
        staff_service.get_staff(db, 999)
