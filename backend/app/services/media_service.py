from sqlalchemy.orm import Session

from app.models.entertainment import Entertainment, MediaType
from app.models.movie import MovieDetails
from app.models.series import SeriesDetails
from app.services.providers.tmdb import TMDBProvider
from app.services.providers.google_books import GoogleBooksProvider


class MediaService:

    def __init__(self, tmdb_provider: TMDBProvider, google_books: GoogleBooksProvider):
        self.tmdb_provider = tmdb_provider
        self.google_books = google_books

    async def import_media(
        self,
        db: Session,
        external_id: str,
        media_type: MediaType
    ):

        # Currently TMDB handles movies and series
        if media_type not in (
            MediaType.MOVIE,
            MediaType.SERIES
        ):
            raise ValueError(
                f"Import for {media_type} is not supported yet"
            )

        # Check whether this media already exists
        existing = (
            db.query(Entertainment)
            .filter(
                Entertainment.external_source == "TMDB",
                Entertainment.external_id == external_id,
                Entertainment.media_type == media_type
            )
            .first()
        )

        if existing:
            return existing

        # -------------------------
        # MOVIE
        # -------------------------

        if media_type == MediaType.MOVIE:

            media_data = await self.tmdb_provider.get_movie_details(
                external_id
            )

            entertainment = Entertainment(
                title=media_data["title"],
                description=media_data.get("description"),
                poster_url=media_data.get("poster_url"),
                release_date=media_data.get("release_date"),
                media_type=MediaType.MOVIE,
                language=media_data.get("language"),
                external_id=media_data["external_id"],
                external_source=media_data["external_source"],
            )

            db.add(entertainment)
            db.flush()

            movie_details = MovieDetails(
                entertainment_id=entertainment.id,
                runtime=media_data.get("runtime"),
                budget=media_data.get("budget"),
                revenue=media_data.get("revenue"),
            )

            db.add(movie_details)

        # -------------------------
        # SERIES
        # -------------------------

        elif media_type == MediaType.SERIES:

            media_data = await self.tmdb_provider.get_series_details(
                external_id
            )

            entertainment = Entertainment(
                title=media_data["title"],
                description=media_data.get("description"),
                poster_url=media_data.get("poster_url"),
                release_date=media_data.get("release_date"),
                media_type=MediaType.SERIES,
                language=media_data.get("language"),
                external_id=media_data["external_id"],
                external_source=media_data["external_source"],
            )

            db.add(entertainment)
            db.flush()

            series_details = SeriesDetails(
                entertainment_id=entertainment.id,
                series_type=media_data["series_type"],
                animation_type=media_data.get("animation_type"),
                number_of_seasons=media_data.get("number_of_seasons"),
                number_of_episodes=media_data.get("number_of_episodes"),
            )

            db.add(series_details)

        db.commit()
        db.refresh(entertainment)

        return entertainment