from fastapi import FastAPI
from sqlalchemy import text
from app.database.database import engine, Base
from app.models.user import User


app = FastAPI(
    title = "Unified Entertainment Platform API",
    version = "1.0.0",
)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"message": "API is working!", "database_connection": "successful"}
    except Exception as e:
        return {"error":str(e)}

