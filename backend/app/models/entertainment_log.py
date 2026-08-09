from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey,
    CheckConstraint
)

from sqlalchemy.orm import relationship

from app.database.database import Base


class EntertainmentLog(Base):
    __tablename__ = "entertainment_logs"

    __table_args__ = (
        CheckConstraint(
            "rating >= 0 AND rating <= 10",
            name="rating_between_0_and_10"
        ),

        CheckConstraint(
            "rating * 2 = CAST(rating * 2 AS INTEGER)",
            name="rating_in_half_steps"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    entertainment_id = Column(
        Integer,
        ForeignKey(
            "entertainment.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    rating = Column(
        Float,
        nullable=True
    )

    review = Column(
        Text,
        nullable=True
    )

    logged_at = Column(
        DateTime,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="entertainment_logs"
    )

    entertainment = relationship(
        "Entertainment",
        back_populates="logs"
    )