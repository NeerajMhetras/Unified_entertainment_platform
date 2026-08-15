from pydantic import BaseModel,ConfigDict
from app.models.entertainment import MediaType
from datetime import date


class MediaImportRequest(BaseModel):
    external_id: str
    media_type: MediaType 


class MediaResponse(BaseModel):
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