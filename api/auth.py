"""
auth.py — Authentication Router

Handles login for Staff (managers and trainers).
On successful login, returns a signed JWT access token.

The token payload contains:
    sub  — staff id (as string)
    role — staff role (manager or trainer)
    gym  — gym id the staff belongs to

Login requires gym_id because email uniqueness is per-gym:
the same email can exist in two different gyms.

Route summary:
    POST /auth/login → verify credentials, return JWT token

Error handling:
    Invalid email or gym_id → 401 Unauthorized
    Wrong password         → 401 Unauthorized
"""

from typing import cast
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.database.session import get_db
from app.repository import staff_repository
from app.core.security import verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["authentication"])


# --- Schemas (auth-specific, not shared with staff CRUD) ---

class LoginRequest(BaseModel):
    """Credentials the client must send to log in."""
    email: EmailStr
    gym_id: int
    password: str


class TokenResponse(BaseModel):
    """JWT token returned on successful login."""
    access_token: str
    token_type: str = "bearer"


# --- Endpoints ---

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Staff login",
    description=(
        "Authenticates a staff member using email, gym_id, and password. "
        "Returns a JWT access token on success. "
        "gym_id is required because the same email can exist in multiple gyms."
    ),
)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a staff member and return a JWT access token.

    Args:
        data: LoginRequest schema — email, gym_id, password.
        db: Database session injected by FastAPI.

    Returns:
        TokenResponse: JWT access token and token type ("bearer").

    Raises:
        HTTPException 401: If the email/gym_id does not match any staff,
                           or if the password is incorrect.
    """
    # Step 1: Look up staff by email within the gym
    staff = staff_repository.get_by_email(db, data.email, data.gym_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Step 2: Verify the password against the stored hash
    hashed = cast(str | None, staff.hashed_password)
    if not hashed or not verify_password(data.password, hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Step 3: Build token payload and return signed JWT
    token = create_access_token({
        "sub": str(staff.id),
        "role": staff.role.value,
        "gym": staff.gym_id,
    })

    return TokenResponse(access_token=token)
