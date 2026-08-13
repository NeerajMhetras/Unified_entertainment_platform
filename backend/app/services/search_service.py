from app.models.entertainment import MediaType
from app.services.providers.tmdb import TMDBProvider

class SearchService:
    def __init__(self, tmdb_provider: TMDBProvider):
        self.tmdb_provider = tmdb_provider

    async def search(
        self,
        query: str,
        media_type: MediaType
    ):
        if media_type == MediaType.MOVIE:
            return await self.tmdb_provider.search_movie(query)

        if media_type == MediaType.SERIES:
            return await self.tmdb_provider.search_series(query)

        raise ValueError(
            f"Search provider not implemented for {media_type}"
        )