import redis

from src.infra.config.app_config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_adapter = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=int(REDIS_DB))
