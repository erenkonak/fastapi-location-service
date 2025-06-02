from fastapi import FastAPI
from app.routers import hello,location

app = FastAPI(
    title="My Professional API",
    description="This is a better structured FastAPI application.",
    version="1.0.0"
)

# Router register
app.include_router(hello.router)
app.include_router(location.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}