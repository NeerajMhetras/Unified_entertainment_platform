from pydantic import BaseModel


class EntertainmentCreate(BaseModel):
    title: str
    media_type: str


class EntertainmentResponse(BaseModel):
    id: int
    title: str
    media_type: str

    model_config = {
        "from_attributes": True
    }