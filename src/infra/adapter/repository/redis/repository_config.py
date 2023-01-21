import redis

from src.infra.config.app_config import REDIS_HOST, REDIS_PORT, REDIS_USER_DB


def get_user_redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_USER_DB)
