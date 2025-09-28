from cachetools import TTLCache
from typing import Any

# Simple in-memory cache for short-lived items (news/weather) to reduce calls
news_cache = TTLCache(maxsize=1024, ttl=900)     # 15 min
weather_cache = TTLCache(maxsize=2048, ttl=900)  # 15 min

def get_cached(cache, key: str) -> Any | None:
    return cache.get(key)

def set_cached(cache, key: str, val: Any):
    cache[key] = val
