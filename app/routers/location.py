from fastapi import APIRouter
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from app.schemas import LocationRequest, LocationAndAnadoluResponse

router = APIRouter(
    prefix="/location",
    tags=["Location"]
)

geolocator = Nominatim(user_agent="my-fastapi-app")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

ANADOLU_YAKASI_ILCELER = [
    "Adalar", "Ataşehir", "Beykoz", "Çekmeköy", "Kadıköy",
    "Kartal", "Maltepe", "Pendik", "Sancaktepe", "Sultanbeyli",
    "Şile", "Tuzla", "Ümraniye", "Üsküdar"
]

@router.post("/", response_model=LocationAndAnadoluResponse)
async def get_location_and_anadolu(address: LocationRequest):
    location = geocode(address.address)
    if not location:
        return {"long": None, "lang": None, "anadoluInd": False}

    lat = location.latitude
    long = location.longitude

    point = (lat, long)
    place = reverse(point, exactly_one=True, language='tr')
    address_details = place.raw.get('address', {})
    
    print(f"Address details: {address_details}")

    district = address_details.get('town') or address_details.get('suburb') or ""
    district = district.strip()

    print(f"District: {district}")
    # Check if the district is in Anadolu Yakası


    is_anadolu = district in ANADOLU_YAKASI_ILCELER

    return {
        "long": long,
        "lang": lat,
        "anadoluInd": is_anadolu
    }