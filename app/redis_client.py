import redis
from .config import settings


redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    db=0,
    decode_responses=True
)


def get_redis():
    return redis_client

redis_client.set("test_key", "hello")
print(redis_client.get("test_key"))