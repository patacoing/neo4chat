from pydantic_settings import BaseSettings


class DbSettings(BaseSettings):
    DB_URI: str = "bolt://localhost:7687"
    DB_USER: str = "neo4j"
    DB_PASSWORD: str = "testtest"


class CacheSettings(BaseSettings):
    CACHE_HOST: str = "localhost"
    CACHE_PASSWORD: str = "test"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    CACHE_TTL: int = 60


class AuthSettings(BaseSettings):
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

class Settings(DbSettings, AuthSettings, CacheSettings, BaseSettings):
    model_config = {
        "env_file": ".env",
    }

settings = Settings()