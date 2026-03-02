"""
progress_repository.py

Repository layer for Progress.
Handles all direct database operations — no business logic lives here.
Progress records track weight, sets, and reps per member per workout per session.
"""

from sqlalchemy.orm import Session
from app.models.progress import Progress
from typing import List


def create(db: Session, progress: Progress) -> Progress:
    """Persist a new Progress record to the database.

    Args:
        db: SQLAlchemy session injected by the caller.
        progress: A Progress model instance (not yet committed).

    Returns:
        The saved Progress with its database-generated id populated.
    """
    db.add(progress)

    db.commit()
    db.refresh(progress)

    return progress


def get_by_id(db: Session, progress_id: int) -> Progress | None:
    """Fetch a single Progress record by its primary key.

    Args:
        db: SQLAlchemy session injected by the caller.
        progress_id: Primary key of the progress record to retrieve.

    Returns:
        The matching Progress, or None if not found.
    """
    return db.query(Progress).filter(Progress.id == progress_id).first()


def get_all(db: Session) -> List[Progress]:
    """Fetch all Progress records in the database.

    Args:
        db: SQLAlchemy session injected by the caller.

    Returns:
        A list of all Progress records (empty list if none exist).
    """
    return db.query(Progress).all()


def get_by_member(db: Session, member_id: int) -> List[Progress]:
    """Fetch all Progress records for a specific member.

    Args:
        db: SQLAlchemy session injected by the caller.
        member_id: Primary key of the member to filter by.

    Returns:
        A list of Progress records for that member (empty list if none exist).
    """
    return db.query(Progress).filter(Progress.member_id == member_id).all()


def get_by_workout(db: Session, workout_id: int) -> List[Progress]:
    """Fetch all Progress records for a specific workout.

    Args:
        db: SQLAlchemy session injected by the caller.
        workout_id: Primary key of the workout to filter by.

    Returns:
        A list of Progress records for that workout (empty list if none exist).
    """
    return db.query(Progress).filter(Progress.workout_id == workout_id).all()


def get_by_session_id(db: Session, session_id: int) -> List[Progress]:
    """Fetch all Progress records logged during a specific workout session.

    Args:
        db: SQLAlchemy session injected by the caller.
        session_id: Primary key of the WorkoutSession to filter by.

    Returns:
        A list of Progress records for that session (empty list if none exist).
    """
    return db.query(Progress).filter(Progress.workout_session_id == session_id).all()


def update(db: Session, progress_id: int, updates: dict) -> Progress | None:
    """Apply a partial update to an existing Progress record.

    Args:
        db: SQLAlchemy session injected by the caller.
        progress_id: Primary key of the progress record to update.
        updates: Dictionary of field names to new values (e.g. {"weight": 100.0}).

    Returns:
        The updated Progress, or None if the record was not found.
    """
    progress = get_by_id(db, progress_id)
    if not progress:
        return None
    for key, value in updates.items():
        setattr(progress, key, value)
    db.commit()
    db.refresh(progress)

    return progress


def delete(db: Session, progress_id: int) -> bool:
    """Delete a Progress record by its primary key.

    Args:
        db: SQLAlchemy session injected by the caller.
        progress_id: Primary key of the progress record to delete.

    Returns:
        True if the record was found and deleted, False if not found.
    """
    progress = get_by_id(db, progress_id)
    if not progress:
        return False
    db.delete(progress)
    db.commit()
    return True
