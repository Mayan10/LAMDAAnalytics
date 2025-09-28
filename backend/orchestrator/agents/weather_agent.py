from ..utils.api_clients import fetch_weather
from ..utils.schema import WeatherFeatures

def detect_anomaly_openweather(payload: dict) -> int:
    # toy detection: daily temp deviation > 1.5 std of week
    try:
        daily = payload.get("daily", [])
        temps = [d["temp"]["day"] for d in daily if "temp" in d]
        if len(temps) >= 5:
            avg = sum(temps)/len(temps)
            var = sum((t-avg)**2 for t in temps)/len(temps)
            std = var ** 0.5
            # if any day deviates > 1.5 std → anomaly
            for t in temps:
                if abs(t-avg) > 1.5*std:
                    return 1
    except Exception:
        pass
    return 0

def detect_anomaly_weatherapi(payload: dict) -> int:
    try:
        days = payload.get("forecast", {}).get("forecastday", [])
        temps = [d["day"]["avgtemp_c"] for d in days if "day" in d]
        if len(temps) >= 5:
            avg = sum(temps)/len(temps)
            var = sum((t-avg)**2 for t in temps)/len(temps)
            std = var ** 0.5
            for t in temps:
                if abs(t-avg) > 1.5*std:
                    return 1
    except Exception:
        pass
    return 0

async def weather_features(lat: float, lon: float) -> WeatherFeatures:
    data = await fetch_weather(lat, lon)
    if not data:
        return WeatherFeatures(weather_anomaly_7d=0, details={})
    # choose detector by payload shape
    anomaly = 1 if ("daily" in data and detect_anomaly_openweather(data)) else detect_anomaly_weatherapi(data)
    return WeatherFeatures(weather_anomaly_7d=anomaly, details={"provider_payload_shape": list(data.keys())})
