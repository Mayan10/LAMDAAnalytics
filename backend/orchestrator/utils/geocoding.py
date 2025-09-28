from .api_clients import geocode

async def resolve_pair(seller_location: str, import_location: str):
    seller = await geocode(seller_location)
    importer = await geocode(import_location)
    return seller, importer
