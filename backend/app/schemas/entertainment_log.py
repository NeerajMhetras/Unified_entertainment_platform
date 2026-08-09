from datetime import datetime

from pydantic import BaseModel, Field


class EntertainmentLogCreate(BaseModel):
    entertainment_id: int

    rating: float | None = Field(
        default=None,
        ge=0,
        le=10
    )

    review: str | None = None

    logged_at: datetime


class EntertainmentLogResponse(BaseModel):
    id: int
    user_id: int
    entertainment_id: int
    rating: float | None
    review: str | None
    logged_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EntertainmentLogUpdate(BaseModel):
    rating: float | None = Field(
        default=None,
        ge=0,
        le=10
    )

    review: str | None = None

    logged_at: datetime | None = None