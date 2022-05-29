from pydantic import BaseSettings, PostgresDsn
from functools import lru_cache


class Settings(BaseSettings):
    # database
    DATABASE_URI: PostgresDsn
    SECRET_KEY: str


@lru_cache()
def get_settings():
    return Settings()
