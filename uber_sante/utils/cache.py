from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

def reset_cache():
    cache.clear()

def get_from_cache(key):
    rv = cache.get(key)
    return rv

def set_to_cache(key, value):
    if key is None:
        return None
    else:
        cache.set(key, value)
