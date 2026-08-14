import httpx

class GoogleBooksProvider:

    BASE_URL = "https://www.googleapis.com/books/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def search_book(self, query: str):

        url = f"{self.BASE_URL}/volumes"

        params = {
            "q": query,
            "key": self.api_key
        }

        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            response = await client.get(
                url,
                params=params
            )

        if response.status_code != 200:
            print("Google Books status:", response.status_code)
            print("Google Books response:", response.text)
        response.raise_for_status()

        data = response.json()

        return self._normalize_search_results(data)

    def _normalize_search_results(self, data: dict):
        results = []
        for item in data.get("items",[]):
            volume = item.get("volumeInfo",{})
            title = volume.get("title")
            if not title:
                continue
            results.append({
                "external_id": item["id"],
                "title": title,
                "description": volume.get("description"),
                "poster_url":(
                    volume.get("imageLinks",{}).get("thumbnail")
                ),
                "release_date": volume.get("publishedDate"),
                "media_type": "book",
                "language": volume.get("language")
            })

        return results