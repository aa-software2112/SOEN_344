cache = {}

def reset_cache():
    cache.clear()

def get_from_cache(key):

    if key is None:
        return None

    rv = cache.get(key)
    return rv

def set_to_cache(key, value):
    if key is None:
        return None
    else:
        cache[key] = value
