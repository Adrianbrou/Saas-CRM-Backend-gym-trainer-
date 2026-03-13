"""
dependency.py — FastAPI Dependencies

Provides reusable dependency functions injected into route handlers via Depends().

Current dependencies:
    get_current_user — decodes the JWT from the Authorization header and returns
                       the authenticated Staff object. Raises 401 if the token is
                       missing, invalid, expired, or the staff no longer exists.

Usage in a route:
    from app.core.dependency import get_current_user

    @router.get("/protected")
    def protected_route(current_user: Staff = Depends(get_current_user)):
        ...
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repository import staff_repository
from app.core import security
from app.models.staff import Staff

# Tells FastAPI where the login endpoint is — powers the "Authorize" button in Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Staff:
    """Decode the JWT access token and return the authenticated Staff member.

    FastAPI automatically extracts the Bearer token from the Authorization header
    and passes it here via oauth2_scheme. The DB session is also injected via get_db.

    Args:
        token: JWT string extracted from the Authorization: Bearer <token> header.
        db: Database session injected by FastAPI.

    Returns:
        Staff: The authenticated staff member object from the database.

    Raises:
        HTTPException 401: If the token is invalid, expired, or the staff does not exist.
    """
    # Step 1: Decode and validate the JWT — raises JWTError if expired or tampered
    try:
        payload = security.decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or has expired",
        )

    # Step 2: Extract staff ID from the "sub" claim (stored as string per JWT standard)
    staff_id = int(payload["sub"])

    # Step 3: Look up the staff in the DB — handles the case where account was deleted
    staff = staff_repository.get_by_id(db, staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return staff
