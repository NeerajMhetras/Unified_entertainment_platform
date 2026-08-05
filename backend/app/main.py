from fastapi import FastAPI
from sqlalchemy import text
from app.database.database import engine, Base
from app.models.user import User
from app.api.routers.user import router as user_router



app = FastAPI(
    title = "Unified Entertainment Platform API",
    version = "1.0.0",
)

app.include_router(user_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
   return {"message": "Backend running"}

