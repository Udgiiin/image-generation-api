from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, validator, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "GenerateImageApi"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = Field(..., env='POSTGRES_HOST')
    DATABASE_URI: Optional[str] = None
    REDIS: Optional[str] = Field(..., env='REDIS')
    ALGORITHM_PASSWORD: str = "sha256"
    IMAGEAPI: str = Field(..., env='IMAGEAPI')
    SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES = 100
    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return "{scheme}://{user}:{password}@{host}/{db}".format(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            db=values.get('POSTGRES_DB'),
            host=values.get('POSTGRES_HOST')
        )

    class Config:
        case_sensitive = True
        env_file = ".env-local"


settings = Settings()
