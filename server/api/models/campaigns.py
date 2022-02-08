from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, DateTime, Integer, String

from api.database import Base


class Campaign(Base):
    """Campaigns Table"""

    __tablename__ = "campaigns"

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)

    user = relationship("User", back_populates="campaigns", foreign_keys=[user_id])

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"{self.id} | {self.name}"
