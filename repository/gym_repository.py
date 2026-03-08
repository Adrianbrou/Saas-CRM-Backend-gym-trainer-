
from sqlalchemy.orm import Session
from app.models.gym import Gym
from typing import List

# create a gym


def create(db: Session, gym: Gym) -> Gym:
    """create funtion (gym): create a function to add more gym to the database 

    args: he function takes 2 parameters
    Session : The Session class we need for type hints correct 
    gym: the Gym model from models
    """
    db.add(gym)  # tells SQLAlchemy to track this new object
    db.commit()  # writes it to the database
    db.refresh(gym)
    # reloads the object from DB so you get the generated id, created_at, etc
    return gym

# fecth one gym by id


def get_by_id(db: Session, gym_id: int) -> Gym | None:
    """fetches a single gym by its id

    db.query(Gym) → "I want to query the gyms table"
    .filter(Gym.id == gym_id) → "WHERE id = gym_id"
    .first() → "give me the first result, or None if not found"

    Args:
        db (Session): The Session class we need for type hints correct 
        gym_id (int): The id we are looking for

    Returns:
        Gym | None: return the gym id if found or None if not exist
    """
    return db.query(Gym).filter(Gym.id == gym_id).first()

# get the gym by name first to help the service layer verify if a gym exist before creating it or not:


def get_by_name(db: Session, name: str) -> Gym | None:
    return db.query(Gym).filter(Gym.name == name).first()

# fetch all gyms


def get_all(db: Session) -> List[Gym]:
    """Fetch all gyms

    Args:
        db (Session): The Session class we need for type hints correct 

    Returns:
        List[Gym]: the list of all the gyms founded
    """
    return db.query(Gym).all()


def update(db: Session, gym_id: int, updates: dict) -> Gym | None:
    """Update an existing gym's fields using a dictionary of changes.
    Fetches the gym by id, then loops over the updates dict and applies
    each field change dynamically using setattr(gym, key, value) —
    which is equivalent to gym.name = value but works for any field name
    passed as a string at runtime. Only the fields present in the dict
    are changed; everything else stays the same.

    Args:
        db (Session): The Session class we need for type hints correct
        gym_id (int): The id we are looking for updating
        updates (dict): dictionary of fields to update e.g. {"name": "FitGym", "location": "Montreal"}

    Returns:
        Gym | None: the new updated gym value  , return none if not founded the id to update
        example: db has(id=23,id=45)
            if you try to update db.id = 90 it return None
            if you try to update db.id = 23 it return the updated gym value oyu replaced since id =23 exist 
    """

    gym = get_by_id(db, gym_id)
    if not gym:
        return None
    for key, value in updates.items():
        setattr(gym, key, value)
    db.commit()
    db.refresh(gym)

    return gym


def delete(db: Session, gym_id: int) -> bool:
    """Deleting a gym based on it's id 

    Args:
        db (Session): _description_
        gym_id (int): _description_

    Returns:
        bool: The response of the deleting action, if it happened ->True else -> False
    """

    gym = get_by_id(db, gym_id)
    if not gym:
        return False
    db.delete(gym)
    db.commit()

    return True
