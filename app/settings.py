from pydantic_settings import BaseSettings


class DbSettings(BaseSettings):
    DB_URI: str = "bolt://localhost:7687"
    DB_USER: str = "neo4j"
    DB_PASSWORD: str = "testtest"

    model_config = {
        "env_file": ".env",
    }


class Settings(DbSettings):
    pass

settings = Settings()