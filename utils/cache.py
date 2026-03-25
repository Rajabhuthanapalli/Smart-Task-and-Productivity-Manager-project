import time

cache_store = {}

def set_cache(key, value, ttl=60):
    expire_time = time.time() + ttl
    cache_store[key] = {
        "value": value,
        "expire_time": expire_time
    }

def get_cache(key):
    data = cache_store.get(key)

    if not data:
        return None

    if time.time() > data["expire_time"]:
        del cache_store[key]
        return None

    return data["value"]
