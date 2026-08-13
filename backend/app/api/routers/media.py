from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session

from app.core.config import settings

from app.database.dependencies import get_db

from app.models.entertainment import MediaType

from app.schemas.search import SearchResult
from app.schemas.entertainment import MediaResponse,MediaImportRequest

from app.services.providers.tmdb import TMDBProvider
from app.services.search_service import SearchService
from app.services.media_service import MediaService

router = APIRouter(
    prefix="/media",
    tags=["Media"]
)


@router.get(
    "/search",
    response_model=list[SearchResult]
)
async def search_media(
    query: str = Query(..., min_length=1),
    media_type: MediaType = Query(...)
):
    provider = TMDBProvider(api_key=settings.TMDB_API_KEY)
    search_service = SearchService(tmdb_provider=provider)

    try:
        return await search_service.search(query=query,media_type=media_type)
    except ValueError as e:
        raise HTTPException(status_code=400,
                            detail=str(e))


@router.post("/import", response_model=MediaResponse)

async def import_media_endpoint(
    request: MediaImportRequest,
    db: Session = Depends(get_db)
):
    tmdb = TMDBProvider(
        api_key=settings.TMDB_API_KEY
    )
    media_service = MediaService(tmdb_provider= tmdb)
    try:
        media = await media_service.import_media(
            db=db,
            external_id=request.external_id,
            media_type=request.media_type
        )
        return media
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))