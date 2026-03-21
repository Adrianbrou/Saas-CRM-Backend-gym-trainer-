from app.services import gym_service
from app.schemas.gym import GymCreate
import pytest


def test_register_gym(db):
    data = GymCreate(name="Test Gym", location="Test City")
    gym = gym_service.register_gym(db, data)
    assert gym.id is not None
    assert gym.name == "Test Gym"


def test_register_duplicate_gym(db):
    data = GymCreate(name="Test Gym", location="Test City")
    gym = gym_service.register_gym(db, data)

    with pytest.raises(ValueError):
        gym_service.register_gym(db, data)
