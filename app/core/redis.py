import redis.asyncio as redis

from app.core.config import settings

redis_client = redis.Redis.from_url(settings.redis_connection_url.render_as_string())

