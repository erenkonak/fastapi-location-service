from pydantic import BaseModel

class HelloResponse(BaseModel):
    message: str


class LocationRequest(BaseModel):
    address: str

class LocationAndAnadoluResponse(BaseModel):
    long: float | None
    lang: float | None
    anadoluInd: bool