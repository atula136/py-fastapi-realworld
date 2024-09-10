import os
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Existing fields
    ENVIRONMENT: str = Field(default="local", env="ENVIRONMENT")
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # MySQL settings only used in non-local environments
    MYSQL_DATABASE: str | None = Field(default=None, env="MYSQL_DATABASE")
    MYSQL_USER: str | None = Field(default=None, env="MYSQL_USER")
    MYSQL_PASSWORD: str | None = Field(default=None, env="MYSQL_PASSWORD")
    MYSQL_ROOT_PASSWORD: str | None = Field(default=None, env="MYSQL_ROOT_PASSWORD")
    DB_PORT: str | None = Field(default=None, env="DB_PORT")

    class Config:
        print("NEIT, ", os.getenv('ENVIRONMENT', 'local'))
        env_file = f".env.{os.getenv('ENVIRONMENT', 'local')}"

    @property
    def is_mysql(self) -> bool:
        return self.ENVIRONMENT in ["dev", "test"]
    
    def get_db_url(self) -> str:
        if self.is_mysql:
            return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@localhost:{self.DB_PORT}/{self.MYSQL_DATABASE}"
        return self.DATABASE_URL

settings = Settings()
