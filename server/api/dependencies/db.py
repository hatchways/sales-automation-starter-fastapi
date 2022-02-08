from typing import Generator
from api.database import SessionLocal


def get_db() -> Generator:
    """Yield a SQLAlchemy database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
