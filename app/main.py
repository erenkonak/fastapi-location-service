from fastapi import FastAPI
from app.routers import hello,location,mail,mail_reader

app = FastAPI(
    title="My Professional API",
    description="This is a better structured FastAPI application.",
    version="1.0.0"
)

# Router register
app.include_router(hello.router)
app.include_router(location.router)
app.include_router(mail.router) 
app.include_router(mail_reader.router)  # <== Add this



@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}