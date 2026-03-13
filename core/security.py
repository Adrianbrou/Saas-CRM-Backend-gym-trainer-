"""
security.py — Authentication & Security Utilities

Provides all cryptographic operations used by the auth layer:
  - Password hashing and verification via bcrypt
  - JWT access token creation and decoding via python-jose

Configuration (required in .env):
    SECRET_KEY  — random secret string used to sign JWT tokens
    ALGORITHM   — signing algorithm, typically "HS256"

Flow:
    REGISTRATION : plain password → hash_password() → store hash in DB
    LOGIN        : plain password + hash from DB → verify_password() → create_access_token()
    REQUEST      : JWT from header → decode_access_token() → get user id → look up in DB
"""

import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

# --- Config guards — fail fast at startup if .env is incomplete ---

ALGORITHM = os.getenv("ALGORITHM", "")
if not ALGORITHM:
    raise ValueError("ALGORITHM not found in .env — set it to 'HS256'")

SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not found in .env — set it to a long random string")

# CryptContext handles bcrypt hashing — .hash() and .verify()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt.

    Args:
        password: The plain-text password received from the client.

    Returns:
        str: A bcrypt hash to store in the database. Never store the plain password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored bcrypt hash.

    Args:
        plain_password: The password the user submitted on login.
        hashed_password: The bcrypt hash stored in the database.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Create a signed JWT access token with a 30-minute expiry.

    Args:
        data: Payload to encode in the token (e.g. {"sub": str(staff_id), "role": "manager"}).

    Returns:
        str: A signed JWT string to send back to the client.
    """
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=30)
    return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token.

    Args:
        token: The JWT string received from the client (Authorization header).

    Returns:
        dict: The decoded payload (e.g. {"sub": "1", "role": "manager", "exp": ...}).

    Raises:
        JWTError: If the token is expired, tampered, or otherwise invalid.
    """
    try:
        return jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise JWTError("Token is invalid or has expired")
