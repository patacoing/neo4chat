import json
from abc import ABC
from typing import Any

from redis import Redis

from app.settings import settings


class CacheInterface(ABC):
    def get(self, key: str) -> str | None:  # pragma: no cover
        ...

    def set(self, key: str, value: str | int, ttl: int) -> None:  # pragma: no cover
        ...

    def set_json(self, key: str, value: Any, ttl: int) -> None:  # pragma: no cover
        ...

    def get_json(self, key: str) -> Any | None:  # pragma: no cover
        ...


class Cache(CacheInterface):
    def __init__(self,
         host: str = settings.CACHE_HOST,
         port: int = settings.CACHE_PORT,
         db: int = settings.CACHE_DB,
         password: str = settings.CACHE_PASSWORD
     ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )

    def get(self, key: str) -> str | None:
        return str(self.redis.get(key))

    def set(self, key: str, value: str | int, ttl: int) -> None:
        self.redis.set(name=key, value=value, ex=ttl)

    def set_json(self, key: str, value: Any, ttl: int) -> None:
        json_str = json.dumps(value)
        self.redis.set(name=key, value=json_str, ex=ttl)

    def get_json(self, key: str) -> Any | None:
        raw_value = self.redis.get(key)
        value: str | None = str(raw_value) if raw_value else None
        if value is None:
            return None

        return json.loads(value)


cache = Cache(
    host=settings.CACHE_HOST,
    port=settings.CACHE_PORT,
    db=settings.CACHE_DB,
    password=settings.CACHE_PASSWORD
)

def get_cache() -> Cache:
    return cache