from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/orchestrator"
    redis_url: str = "redis://localhost:6379/0"
    log_level: str = "INFO"
    max_retries: int = 3
    retry_delay: int = 60
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
