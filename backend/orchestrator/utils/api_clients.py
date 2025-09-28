import httpx
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
from ..utils.timeutils import utc_now_iso
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.settings import settings

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)

def get_gemini():
    # Change model if you want a different Gemini variant
    return genai.GenerativeModel("gemini-2.0-flash")

def http_client():
    return httpx.AsyncClient(timeout=settings.http_timeout_seconds)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=4))
async def serp_search(query: str, num: int = 10) -> dict:
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": query,
        "num": num,
        "api_key": settings.serp_api_key,
        "hl": "en",
        "gl": "us"
    }
    async with http_client() as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()

async def geocode(address: str) -> tuple[float, float] | None:
    base = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": settings.google_maps_api_key}
    async with http_client() as client:
        r = await client.get(base, params=params)
        r.raise_for_status()
        data = r.json()
        if data.get("results"):
            loc = data["results"][0]["geometry"]["location"]
            return (loc["lat"], loc["lng"])
    return None

async def fetch_openweather(lat: float, lon: float) -> dict | None:
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat, "lon": lon, "appid": settings.weather_api_key,
        "exclude": "minutely,hourly,alerts"
    }
    async with http_client() as client:
        r = await client.get(url, params=params)
        if r.status_code == 200:
            return r.json()
    return None

async def fetch_weatherapi(lat: float, lon: float) -> dict | None:
    # Map lat/lon to a query string as provider expects city names; here we pass coord
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": settings.weather_api_key, "q": f"{lat},{lon}", "days": 7, "aqi": "no", "alerts": "no"
    }
    async with http_client() as client:
        r = await client.get(url, params=params)
        if r.status_code == 200:
            return r.json()
    return None

async def fetch_weather(lat: float, lon: float) -> dict | None:
    if settings.weather_provider.lower() == "weatherapi":
        return await fetch_weatherapi(lat, lon)
    return await fetch_openweather(lat, lon)

async def gemini_structured(prompt: str) -> dict:
    """Ask Gemini to return strict JSON. If parsing fails, return {}."""
    model = get_gemini()
    resp = model.generate_content(
        [{"text": prompt}],
        generation_config={"response_mime_type": "application/json"}
    )
    try:
        import json
        return json.loads(resp.text)
    except Exception:
        # Best effort: try to parse JSON-like string
        import json, re
        try:
            return json.loads(resp.text)
        except Exception:
            try:
                # strip code block fences
                s = re.sub(r"```json|```", "", resp.text).strip()
                return json.loads(s)
            except Exception:
                return {}
