"""
workout_session_repository.py

Repository layer for WorkoutSession.
Handles all direct database operations — no business logic lives here.
Sessions are tenant-scoped: all queries that return multiple records filter by gym_id.
"""

from app.models.workout_session import WorkoutSession
from sqlalchemy.orm import Session
from typing import List


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------

def create(db: Session, workout_session: WorkoutSession) -> WorkoutSession:
    """Persist a new WorkoutSession to the database.

    Args:
        db: SQLAlchemy session injected by the caller.
        workout_session: A WorkoutSession model instance (not yet committed).

    Returns:
        The saved WorkoutSession with its database-generated id populated.
    """
    db.add(workout_session)
    db.commit()
    db.refresh(workout_session)
    return workout_session


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------

def get_by_id(db: Session, workout_session_id: int) -> WorkoutSession | None:
    """Fetch a single WorkoutSession by its primary key.

    Args:
        db: SQLAlchemy session injected by the caller.
        workout_session_id: Primary key of the session to retrieve.

    Returns:
        The matching WorkoutSession, or None if not found.
    """
    return db.query(WorkoutSession).filter(
        WorkoutSession.id == workout_session_id).first()


def get_all(db: Session, gym_id: int) -> List[WorkoutSession]:
    """Fetch all WorkoutSessions belonging to a specific gym.

    Sessions are tenant-scoped, so gym_id is always required.

    Args:
        db: SQLAlchemy session injected by the caller.
        gym_id: ID of the gym (tenant) to filter by.

    Returns:
        A list of WorkoutSessions for that gym (empty list if none exist).
    """
    return db.query(WorkoutSession).filter(WorkoutSession.gym_id == gym_id).all()


def get_by_trainer(db: Session, trainer_id: int) -> List[WorkoutSession]:
    """Fetch all WorkoutSessions led by a specific trainer (staff member).

    Used by the service layer to retrieve a trainer's full session history.

    Args:
        db: SQLAlchemy session injected by the caller.
        trainer_id: The staff_id of the trainer to filter by.

    Returns:
        A list of WorkoutSessions assigned to that trainer (empty list if none).
    """
    return db.query(WorkoutSession).filter(WorkoutSession.staff_id == trainer_id).all()


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------

def update(db: Session, workout_session_id: int, updates: dict) -> WorkoutSession | None:
    """Apply a partial update to an existing WorkoutSession.

    Args:
        db: SQLAlchemy session injected by the caller.
        workout_session_id: Primary key of the session to update.
        updates: Dictionary of field names to new values (e.g. {"scheduled_at": ...}).

    Returns:
        The updated WorkoutSession, or None if the session was not found.
    """
    workout_session = get_by_id(db, workout_session_id)
    if not workout_session:
        return None

    for key, value in updates.items():
        setattr(workout_session, key, value)

    db.commit()
    db.refresh(workout_session)
    return workout_session


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------

def delete(db: Session, workout_session_id: int) -> bool:
    """Delete a WorkoutSession by its primary key.

    Cascades will remove related Attendance, SessionWorkouts, and Progress
    records automatically (defined on the DB level with ondelete="CASCADE").

    Args:
        db: SQLAlchemy session injected by the caller.
        workout_session_id: Primary key of the session to delete.

    Returns:
        True if the session was found and deleted, False if not found.
    """
    workout_session = get_by_id(db, workout_session_id)
    if not workout_session:
        return False

    db.delete(workout_session)
    db.commit()
    return True
