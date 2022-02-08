from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import BigInteger, DateTime, String

from api.database import Base


class User(Base):
    """Users Table"""

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_digest = Column(String, unique=True, index=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    prospects = relationship("Prospect", back_populates="user")
    campaigns = relationship("Campaign", back_populates="user")

    def __repr__(self):
        return f"{self.id} | {self.email}"
