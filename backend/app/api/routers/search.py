from fastapi import APIRouter, HTTPException, Query

from app.models.entertainment import MediaType
from app.schemas.search import SearchResult
from app.services.providers.tmdb import TMDBProvider
from app.core.config import settings


router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get(
    "/",
    response_model=list[SearchResult]
)
async def search_entertainment(
    query: str = Query(..., min_length=1),
    media_type: MediaType = Query(...)
):
    if media_type == MediaType.MOVIE:

        provider = TMDBProvider(
            api_key=settings.TMDB_API_KEY
        )

        return await provider.search_movie(query)

    raise HTTPException(
        status_code=400,
        detail=f"Search for {media_type} is not supported yet"
    )