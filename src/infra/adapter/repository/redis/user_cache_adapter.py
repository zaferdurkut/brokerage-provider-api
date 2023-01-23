from src.infra.adapter.repository.redis.repository_config import get_user_redis_client


class UserCacheAdapter:
    def __init__(self):
        self.client = get_user_redis_client()
