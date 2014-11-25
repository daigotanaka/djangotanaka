from django.core.cache import cache


def cache_get_key(*args, **kwargs):
    """Get the cache key for storage"""
    import hashlib
    serialise = []
    for arg in args:
        serialise.append(str(arg))
    for key,arg in kwargs.items():
        if key == "clear_cache":
            continue
        serialise.append(str(key))
        serialise.append(str(arg))
    key = hashlib.md5("".join(serialise)).hexdigest()
    return key


def cache_for(time):
    """Decorator for caching functions"""
    def decorator(fn):
        def wrapper(*args, **kwargs):
            key = cache_get_key(fn.__name__, *args, **kwargs)
            result = cache.get(key)
            if not result or "clear_cache" in kwargs and kwargs["clear_cache"]:
                cache.delete(key)
                result = fn(*args, **kwargs)
                cache.set(key, result, time)
            return result + "<!-- cache key: %s -->" % key
        return wrapper
    return decorator
