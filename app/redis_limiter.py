from fastapi import HTTPException, status
from .redis_client import redis_client


def check_rate_limit(user_id: int, limit: int, window: int):
    key = f"rate_limit:{user_id}"
    
    pipe = redis_client.pipeline()
    pipe.incr(key)
    pipe.expire(key, window, nx=True) 
    results = pipe.execute()
    
    current_count = results[0]

    if current_count > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later."
        )