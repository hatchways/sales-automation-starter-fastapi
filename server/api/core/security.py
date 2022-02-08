from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session

from .config import settings
from api import schemas
from api.models import User
from api.crud.user import UserCrud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(data: dict) -> str:
    """Create a JWT (access token) based on the provided data"""
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, password_digest: str) -> bool:
    """Check that hashed(plain_password) matches password_digest."""
    return pwd_context.verify(plain_password, password_digest)


def get_password_hash(password: str) -> str:
    """Return the hashed version of password"""
    return pwd_context.hash(password)


def decode_token(token: str) -> schemas.Token:
    """Return a dictionary that represents the decoded JWT."""
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    return schemas.Token(**decoded)


async def authenticate_user(
    db: Session, email: str, password: str
) -> Union[bool, User]:
    """Based on the provided email & password, verify that the credentials match
    the records contained in the database.
    """
    user = UserCrud.get_user_by_email(db, email)
    if not user:
        # No user with that email exists in the database
        return False
    if not verify_password(password, user.password_digest):
        # The user exists but the password was incorrect
        return False
    return user
