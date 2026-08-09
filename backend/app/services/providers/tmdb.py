import httpx


class TMDBProvider:

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def search_movie(self, query: str):
        url = "https://api.themoviedb.org/3/search/movie"

        params = {
            "api_key": self.api_key,
            "query": query
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params=params
            )

        response.raise_for_status()

        return response.json()