
from app.schemas.member import MemberCreate
from app.services import gym_service
from app.services import member_service
from app.schemas.gym import GymCreate
import pytest


def test_register_member(db):
    data_gym = GymCreate(name="Test Gym", location="Test City")
    gym = gym_service.register_gym(db, data_gym)

    data_member = MemberCreate(
        gym_id=gym.id, name="mark", email="mark@gmail.com", phone="234445234")

    member = member_service.register_member(db, data_member)

    assert member.id is not None
    assert member.name == "mark"
    assert member.gym_id == gym.id


def test_register_duplicate_member(db):
    data_gym = GymCreate(name="Test Gym", location="Test City")
    gym = gym_service.register_gym(db, data_gym)

    data_member = MemberCreate(
        gym_id=gym.id, name="mark", email="mark@gmail.com", phone="234445234")

    member_service.register_member(db, data_member)

    with pytest.raises(ValueError):
        member_service.register_member(db, data_member)


def test_member_not_found(db):
    with pytest.raises(ValueError):
        member_service.get_member(db, 89)
