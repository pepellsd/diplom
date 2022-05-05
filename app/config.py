from pydantic import BaseSettings, PostgresDsn
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # database
    DATABASE_URI: PostgresDsn
    SECRET_KEY: str

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings():
    return Settings()
