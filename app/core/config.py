import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Existing fields
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Add any extra environment variables you need
    ENVIRONMENT: str = "local"
    MYSQL_DATABASE: str = None
    MYSQL_USER: str = None
    MYSQL_PASSWORD: str = None
    MYSQL_ROOT_PASSWORD: str = None
    DB_PORT: str = None

    class Config:
        env_file = f".env.{os.getenv('ENVIRONMENT', 'local')}"

settings = Settings()
