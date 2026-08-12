from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.config import settings

from app.schemas.entertainment import MovieImportRequest
from app.services.providers.tmdb import TMDBProvider
from app.services.entertainment_service import import_movie
from app.schemas.entertainment import EntertainmentResponse


router = APIRouter(
    prefix="/entertainment",
    tags=["Entertainment"]
)


@router.post("/import/movie", response_model=EntertainmentResponse)
async def import_movie_endpoint(
    request: MovieImportRequest,
    db: Session = Depends(get_db)
):
    tmdb = TMDBProvider(
        api_key=settings.TMDB_API_KEY
    )

    movie = await import_movie(
        db=db,
        tmdb=tmdb,
        external_id=request.external_id
    )

    