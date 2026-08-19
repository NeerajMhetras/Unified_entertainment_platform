from fastapi import FastAPI
from sqlalchemy import text
from app.database.database import engine, Base

from app.api.routers.auth import router as auth_router
from app.api.routers.user import router as user_router
from app.api.routers.entertainment_log import router as entertainment_log_router
from app.api.routers.media import router as entertainment_router


from app.models.user import User
from app.models.entertainment import Entertainment
from app.models.movie import MovieDetails
from app.models.series import SeriesDetails
from app.models.game import GameDetails,Platform
from app.models.book import BookDetails, Author
from app.models.entertainment_log import EntertainmentLog




app = FastAPI(
    title = "Unified Entertainment Platform API",
    version = "1.0.0",
)

app.include_router(user_router)
app.include_router(entertainment_log_router)
app.include_router(entertainment_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)



@app.get("/")
async def root():
   return {"message": "Backend running"}

