from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "GenerateImageApi"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: Optional[str] = None
    REDIS: Optional[str] = "redis"
    ALGORITHM: str
    IMAGEAPI: str
    SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES = 100
    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return "{scheme}://{user}:{password}@db/{db}".format(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            db=values.get('POSTGRES_DB'),
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
