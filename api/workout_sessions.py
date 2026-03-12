"""
workout_sessions.py — Workout Sessions API Router

Handles all HTTP endpoints for WorkoutSession and Attendance resources.
Sessions are gym-scoped: every session belongs to a gym via gym_id.
A session must be assigned to a trainer (Staff) who belongs to the same gym.
Attendance links members to sessions via a junction table.

Route summary:
    POST   /workout-sessions/                                    → create a new session
    GET    /workout-sessions/gyms/{gym_id}                       → list all sessions for a gym
    POST   /workout-sessions/{session_id}/members                → add a member to a session
    DELETE /workout-sessions/{session_id}/members/{member_id}    → remove a member from a session

Error handling:
    ValueError from service layer → 400 Bad Request (not found or gym mismatch)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services import workout_session_service
from app.schemas.workout_session import (
    WorkoutSessionCreate,
    WorkoutSessionResponse,
    AttendanceCreate,
    AttendanceResponse,
)


router = APIRouter(prefix="/workout-sessions", tags=["workout-sessions"])


@router.post(
    "/",
    response_model=WorkoutSessionResponse,
    summary="Create a new workout session",
    description=(
        "Creates a new workout session for a gym. "
        "The assigned trainer (staff_id) must belong to the same gym as the session. "
        "A trainer from another gym cannot lead a session."
    ),
)
def create_session(data: WorkoutSessionCreate, db: Session = Depends(get_db)):
    """Create a new workout session.

    Args:
        data: WorkoutSessionCreate schema — gym_id, staff_id, scheduled_at.
        db: Database session injected by FastAPI.

    Returns:
        WorkoutSessionResponse: The newly created session including id and timestamps.

    Raises:
        HTTPException 400: If the trainer does not exist or does not belong to this gym.
    """
    try:
        return workout_session_service.create_session(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/gyms/{gym_id}",
    response_model=list[WorkoutSessionResponse],
    summary="List all sessions for a gym",
    description="Returns every workout session scheduled for the given gym. May return an empty list.",
)
def get_all(gym_id: int, db: Session = Depends(get_db)):
    """Retrieve all workout sessions for a specific gym.

    Args:
        gym_id: Primary key of the gym to query.
        db: Database session injected by FastAPI.

    Returns:
        list[WorkoutSessionResponse]: All sessions for that gym (may be empty).
    """
    return workout_session_service.get_all(db, gym_id)


@router.post(
    "/{session_id}/members",
    response_model=AttendanceResponse,
    summary="Add a member to a session",
    description=(
        "Registers a member as attending a workout session. "
        "Both the session and the member must already exist."
    ),
)
def add_member(session_id: int, data: AttendanceCreate, db: Session = Depends(get_db)):
    """Add a member to a workout session.

    Args:
        session_id: Primary key of the session (used for route clarity — also in data).
        data: AttendanceCreate schema — workout_session_id, member_id.
        db: Database session injected by FastAPI.

    Returns:
        AttendanceResponse: The created attendance record linking member to session.

    Raises:
        HTTPException 400: If the session or member does not exist.
    """
    try:
        return workout_session_service.add_member_to_session(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{session_id}/members/{member_id}",
    response_model=bool,
    summary="Remove a member from a session",
    description=(
        "Removes a member's attendance record from a workout session. "
        "Returns True if removed, False if the member was not in the session."
    ),
)
def remove_member(session_id: int, member_id: int, db: Session = Depends(get_db)):
    """Remove a member from a workout session.

    Args:
        session_id: Primary key of the workout session.
        member_id: Primary key of the member to remove.
        db: Database session injected by FastAPI.

    Returns:
        bool: True if the attendance record was deleted, False if not found.

    Raises:
        HTTPException 400: If the session does not exist.
    """
    try:
        return workout_session_service.remove_member_from_session(db, session_id, member_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
