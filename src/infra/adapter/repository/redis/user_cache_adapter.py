from src.infra.adapter.repository.redis.repository_config import get_user_redis_client


class UserCacheAdapter:
    def __init__(self):
        self.client = get_user_redis_client()

    def set(self, key, value, expires: int):
        result = self.client.set(key, value, ex=expires)
        return result

    def setex(self, key, value, expires: int):
        result = self.client.setex(key, expires, value)
        return result

    def get(self, key):
        result = self.client.get(key)
        return result

    def exist(self, key):
        result = self.client.exists(key)
        return result

    def get_all_key(self):
        keys = []
        for key in self.client.scan_iter(match="*"):
            keys.append(key)

        return keys

    def delete_key(self, key):
        self.client.delete(key)

    def delete_all_key(
        self,
    ):
        for key in self.client.scan_iter(match="*"):
            self.client.delete(key)

    def delete_all_key_from_search(self, search_item: str):
        for key in self.client.scan_iter(match=f"*{search_item}*"):
            self.client.delete(key)
