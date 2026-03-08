"""
progress.py — Pydantic Schemas for Progress

Progress records track performance per member per workout per session.
Foreign keys (member_id, workout_id, workout_session_id) are not updatable —
changing them would mean a different record. Only performance values can be updated.
"""

from pydantic import BaseModel
from datetime import datetime


class ProgressCreate(BaseModel):
    """Fields the client must send when logging a new progress record.

    All three foreign keys are required to link the record to a member,
    a specific workout, and the session it was performed in.
    """
    member_id: int
    workout_id: int
    workout_session_id: int
    weight_kg: float
    sets: int
    reps: int


class ProgressUpdate(BaseModel):
    """Fields the client may send when correcting a progress record.

    Only performance values are updatable. Foreign keys are excluded —
    if the wrong member/workout/session was used, delete and recreate.
    """
    weight_kg: float | None = None
    sets: int | None = None
    reps: int | None = None


class ProgressResponse(BaseModel):
    """Full progress data returned by the API after any successful operation."""
    id: int
    member_id: int
    workout_id: int
    workout_session_id: int
    weight_kg: float
    sets: int
    reps: int
    logged_at: datetime
    model_config = {"from_attributes": True}
