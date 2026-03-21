"""
workout_service.py — Business Logic for Workout and BodyPart

Workouts are NOT gym-scoped — they are shared across all gyms.
A workout must be linked to an existing BodyPart (e.g. Chest, Legs).
Workout names must be unique across the entire system.
"""

from app.models.workout import Workout
from app.repository import workout_repository
from app.schemas.workout import WorkoutCreate, WorkoutUpdate
from sqlalchemy.orm import Session


def create_workout(db: Session, data: WorkoutCreate) -> Workout:
    """Create a new workout after verifying the name is not already taken.

    Business rules enforced:
      - Workout names must be unique system-wide (not per gym)

    Args:
        db: SQLAlchemy session injected by the caller.
        data: Validated WorkoutCreate schema (name, body_part_id).

    Raises:
        ValueError: If a workout with the same name already exists.

    Returns:
        The newly created Workout with database-generated id.
    """
    # Check duplicate name — workouts are global, names must be unique
    existing = db.query(Workout).filter(Workout.name == data.name).first()
    if existing:
        raise ValueError("Workout with this name already exists")

    workout = Workout(**data.model_dump())
    return workout_repository.create(db, workout)


def get_workout(db: Session, workout_id: int) -> Workout:
    """Retrieve a workout by id after verifying it exists.

    Args:
        db: SQLAlchemy session injected by the caller.
        workout_id: Primary key of the workout to retrieve.

    Raises:
        ValueError: If no workout with that id exists.

    Returns:
        The matching Workout object.
    """
    existing = workout_repository.get_by_id(db, workout_id)
    if not existing:
        raise ValueError("Workout not found")
    return existing


def get_all(db: Session, skip: int = 0, limit: int = 20) -> list[Workout]:
    """this function is the retrieve the all Workouts information  from the db
    Args:
        db (Session): Session to the database
        skip (int): Number of records to skip. Defaults to 0.
        limit (int): Maximum number of records to return. Defaults to 20.

    Returns:
        all Workouts found as list
    """

    return workout_repository.get_all(db, skip=skip, limit=limit)


def update_workout(db: Session, workout_id: int, data: WorkoutUpdate) -> Workout:
    """Update an existing workout's fields after verifying it exists.

    Args:
        db: SQLAlchemy session injected by the caller.
        workout_id: Primary key of the workout to update.
        data: Validated WorkoutUpdate schema — all fields optional.

    Raises:
        ValueError: If no workout with that id exists.

    Returns:
        The updated Workout with new values reflected.
    """
    existing = workout_repository.get_by_id(db, workout_id)
    if not existing:
        raise ValueError("Workout not found")

    # Only update fields the client actually sent
    updates = data.model_dump(exclude_unset=True)
    return workout_repository.update(db, workout_id, updates)


def delete_workout(db: Session, workout_id: int) -> bool:
    """Delete a workout after verifying it exists.

    Args:
        db: SQLAlchemy session injected by the caller.
        workout_id: Primary key of the workout to delete.

    Raises:
        ValueError: If no workout with that id exists.

    Returns:
        True if the workout was found and deleted.
    """
    existing = workout_repository.get_by_id(db, workout_id)
    if not existing:
        raise ValueError("Workout not found")
    return workout_repository.delete(db, workout_id)
