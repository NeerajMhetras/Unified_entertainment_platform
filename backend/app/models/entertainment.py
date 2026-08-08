from enum import Enum

from sqlalchemy import Column, Integer, String, Text, Date, Enum as SQLEnum

from app.database.database import Base


class MediaType(str, Enum):
    MOVIE = "movie"
    SERIES = "series"
    BOOK = "book"
    GAME = "game"


class Entertainment(Base):
    __tablename__ = "entertainment"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    description = Column(Text, nullable=True)

    poster_url = Column(String(500), nullable=True)

    release_date = Column(Date, nullable=True)

    media_type = Column(
        SQLEnum(MediaType),
        nullable=False
    )

    language = Column(String(50), nullable=True)

    external_id = Column(String(100), nullable=True)

    external_source = Column(String(50), nullable=True)