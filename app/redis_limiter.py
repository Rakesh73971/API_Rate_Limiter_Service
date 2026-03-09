from fastapi import HTTPException, status
from .redis_client import redis_client


def check_rate_limit(user_id: int, limit: int, window: int):

    key = f"rate_limit:{user_id}"

    current = redis_client.get(key)

    if current and int(current) >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )

    redis_client.incr(key)

    if int(redis_client.get(key)) == 1:
        redis_client.expire(key, window)