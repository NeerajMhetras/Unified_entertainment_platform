from sqlalchemy.orm import Session

from app.models.entertainment import Entertainment, MediaType
from app.models.movie import MovieDetails
from app.services.providers.tmdb import TMDBProvider


class MediaService:

    def __init__(self, tmdb_provider: TMDBProvider):
        self.tmdb_provider = tmdb_provider

    def get_provider(self, media_type: MediaType):

        if media_type in (
            MediaType.MOVIE,
            MediaType.SERIES
        ):
            return self.tmdb_provider

        raise ValueError(
            f"Provider for {media_type} is not supported yet"
        )

    async def import_media(
        self,
        db: Session,
        external_id: str,
        media_type: MediaType
    ):
        provider = self.get_provider(media_type)

        if media_type == MediaType.MOVIE:

            existing = (
                db.query(Entertainment)
                .filter(
                    Entertainment.external_source == "TMDB",
                    Entertainment.external_id == external_id
                )
                .first()
            )

            if existing:
                return existing

            movie_data = await provider.get_movie_details(
                external_id
            )

            entertainment = Entertainment(
                title=movie_data["title"],
                description=movie_data.get("description"),
                poster_url=movie_data.get("poster_url"),
                release_date=movie_data.get("release_date"),
                media_type=MediaType.MOVIE,
                language=movie_data.get("language"),
                external_id=movie_data["external_id"],
                external_source=movie_data["external_source"],
            )

            db.add(entertainment)
            db.flush()

            movie_details = MovieDetails(
                entertainment_id=entertainment.id,
                runtime=movie_data.get("runtime"),
                budget=movie_data.get("budget"),
                revenue=movie_data.get("revenue"),
            )

            db.add(movie_details)

            db.commit()
            db.refresh(entertainment)

            return entertainment

        raise ValueError(
            f"Import for {media_type} is not implemented yet"
        )