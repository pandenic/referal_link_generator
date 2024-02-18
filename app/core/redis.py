"""Settings for redis connection and interaction with it."""
import pickle

import redis.asyncio as redis

from app.core.config import settings

redis_client = redis.Redis.from_url(
    settings.redis_connection_url.render_as_string(),
)


async def get_referral_redis(field):
    """
    Get a ReferralCode obj from redis cache.

    by referrer_id
    or
    by referral code
    """
    await redis_client.get(
        f"referral_{field}",
    )


async def delete_referral_redis(db_obj):
    """
    Delete a ReferralCode obj from redis cache.

    by referrer_id
    by referral code
    """
    await redis_client.delete(
        f"referral_{db_obj.referrer_id}",
        f"referral_{db_obj.code}",
    )


async def set_referral_redis(db_obj):
    """
    Set a ReferralCode obj to redis cache.

    by referrer_id
    by referral code
    """
    await redis_client.mset(
        {
            f"referral_{db_obj.referrer_id}": pickle.dumps(db_obj),
            f"referral_{db_obj.code}": pickle.dumps(db_obj),
        },
    )
