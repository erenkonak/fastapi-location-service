from fastapi import APIRouter
from app.schemas import HelloResponse

router = APIRouter(
    prefix="/hello",
    tags=["Hello Operations"]
)

@router.get("/", response_model=HelloResponse)
async def say_hello(name: str = "World"):
    return {"message": f"Hello, {name}!"}