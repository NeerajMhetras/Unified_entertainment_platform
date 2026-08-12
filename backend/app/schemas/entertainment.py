from pydantic import BaseModel,ConfigDict
from app.models.entertainment import MediaType
from datetime import date


class MovieImportRequest(BaseModel):
    external_id: str


class EntertainmentResponse(BaseModel):
    id: int
    title: str
    description: str | None
    poster_url: str | None
    release_date: date | None
    media_type: MediaType
    language: str | None
    external_id: str | None
    external_source: str | None

    model_config = ConfigDict(
        from_attributes=True
    )