from functools import wraps
import hashlib

from common.connectors.redis_helper import Redis

redis = Redis()


def redis_cache(ttl=60):
    """
    Cache function result in Redis if not exists
    :param ttl: time-to-live in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key_value=f"{func.__name__}:{args}"
            key=hashlib.md5(key_value.encode()).hexdigest()
            # 1. Check cache
            cached_data = redis.retrieve_data(key)
            if cached_data is not None:
                return cached_data

            # 2. Call function
            result = func(*args, **kwargs)
            if result!='Failed to convert url':
                redis.insert_data(key,result,expiry=ttl)
          
            return result
        return wrapper
    return decorator

def redis_async_cache(ttl=60):
    """
    Cache function result in Redis if not exists
    :param ttl: time-to-live in seconds
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key_value=f"{func.__name__}:{args}"
            key=hashlib.md5(key_value.encode()).hexdigest()
            # 1. Check cache
            cached_data = redis.retrieve_data(key)
            if cached_data is not None:
                return cached_data

            # 2. Call function
            result = await func(*args, **kwargs)
            if result!='Failed to convert url':
                redis.insert_data(key,result,expiry=ttl)
          
            return result
        return wrapper
    return decorator
