from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim

async with Nominatim(
    user_agent="specify_your_app_name_here",
    adapter_factory=AioHTTPAdapter,
) as geolocator:
    location = await geolocator.geocode("175 5th Avenue NYC")
    print(location.address)