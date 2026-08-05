from fastapi import FastAPI

app = FastAPI(
    title = "Unified Entertainment Platform API",
    version = "1.0.0",
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Unified Entertainment Platform API!"}
