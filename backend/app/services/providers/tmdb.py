import httpx

from app.schemas.search import SearchResult
from app.models.entertainment import MediaType


class TMDBProvider:

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def search_movie(self, query: str):
        url = "https://api.themoviedb.org/3/search/movie"

        params = {
            "api_key": self.api_key,
            "query": query
        }

        transport = httpx.AsyncHTTPTransport(
            local_address="0.0.0.0"
        )

        async with httpx.AsyncClient(
            transport=transport,
            timeout=30.0
        ) as client:
            response = await client.get(
                url,
                params=params
            )

        response.raise_for_status()

        data = response.json()

        return [
            self._normalize_movie(movie)
            for movie in data["results"]
        ]
    def _normalize_movie(self, movie: dict) -> SearchResult:

        poster_path = movie.get("poster_path")

        poster_url = None

        if poster_path:
            poster_url = (
                "https://image.tmdb.org/t/p/w500"
                + poster_path
            )

        return SearchResult(
            external_id=str(movie["id"]),
            title=movie["title"],
            media_type=MediaType.MOVIE,
            description=movie.get("overview"),
            release_date=movie.get("release_date"),
            poster_url=poster_url
        )