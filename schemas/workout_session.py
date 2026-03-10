"""
workout_session.py — Pydantic Schemas for WorkoutSession, Attendance, SessionWorkouts

Three models live here — all are gym-scoped and session-scoped.
Attendance and SessionWorkouts are junction tables: no Update schemas needed.
"""

from pydantic import BaseModel
from datetime import datetime


class WorkoutSessionCreate(BaseModel):
    """Fields the client must send when creating a new workout session.

    gym_id scopes the session to a gym. staff_id assigns a trainer.
    scheduled_at is required — sessions must have a scheduled time.
    """
    gym_id: int
    staff_id: int
    scheduled_at: datetime


class WorkoutSessionUpdate(BaseModel):
    """Fields the client may send when updating a workout session.

    gym_id excluded — sessions cannot be moved between gyms.
    Only the trainer or schedule can be changed.
    """
    staff_id: int | None = None
    scheduled_at: datetime | None = None


class WorkoutSessionResponse(BaseModel):
    """Full session data returned by the API after any successful operation."""
    id: int
    gym_id: int
    staff_id: int
    scheduled_at: datetime
    created_at: datetime
    updated_at: datetime | None = None
    model_config = {"from_attributes": True}


class AttendanceCreate(BaseModel):
    """Fields the client must send when adding a member to a session."""
    workout_session_id: int
    member_id: int


class AttendanceResponse(BaseModel):
    """Attendance record returned by the API — links a member to a session."""
    workout_session_id: int
    member_id: int
    model_config = {"from_attributes": True}


class SessionWorkoutsCreate(BaseModel):
    """Fields the client must send when adding a workout to a session."""
    workout_session_id: int
    workout_id: int


class SessionWorkoutsResponse(BaseModel):
    """SessionWorkout record returned by the API — links a workout to a session."""
    workout_session_id: int
    workout_id: int
    model_config = {"from_attributes": True}
