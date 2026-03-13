from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

import os

from dotenv import load_dotenv

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
if not ALGORITHM:
    raise ValueError("algoritm not existing in .env")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("secret key not existing in .env")
pwd_context = CryptContext(schemes=["bcrypt"])
# pwd_context has two methods — .hash() and .verify()
# Hash a password


def hash_password(password: str) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password
# Verify a password against a hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
# Create a JWT token


def create_access_token(data: dict) -> str:
    copy_of_data = data.copy()
    copy_of_data["exp"] = datetime.now(timezone.utc) + timedelta(minutes=30)
    return jwt.encode(copy_of_data, key=SECRET_KEY, algorithm=ALGORITHM)

# Decode/validate a JWT token


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise JWTError("Token is invalid or has expired")
