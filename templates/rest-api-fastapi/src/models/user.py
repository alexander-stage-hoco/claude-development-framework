"""
User SQLAlchemy Model

Database model for User entity.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.db.database import Base


class User(Base):
    """
    User model.

    Represents a user in the system with email/password authentication.
    """

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    hashed_password = Column(
        String(255),
        nullable=False,
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
