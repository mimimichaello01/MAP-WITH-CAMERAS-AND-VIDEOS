from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, BaseModel

BASE_DIR = Path(__file__).parent.parent


class DatabaseSettings(BaseSettings):
    POSTGRES_DB: str = Field(validation_alias="POSTGRES_DB")
    POSTGRES_USER: str = Field(validation_alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(validation_alias="POSTGRES_PASSWORD")
    POSTGRES_PORT: str = Field(default="5432", validation_alias="POSTGRES_PORT")
    POSTGRES_HOST: str = Field(default="localhost", validation_alias="POSTGRES_HOST")

    def build_async_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"


class MinioSettings(BaseSettings):
    MINIO_ENDPOINT: str = Field(validation_alias="MINIO_ENDPOINT")
    MINIO_PUBLIC_ENDPOINT: str = Field(validation_alias="MINIO_PUBLIC_ENDPOINT")
    MINIO_ROOT_USER: str = Field(validation_alias="MINIO_ROOT_USER")
    MINIO_ROOT_PASSWORD: str = Field(validation_alias="MINIO_ROOT_PASSWORD")
    MINIO_BUCKET: str = Field(default="media", validation_alias="MINIO_BUCKET")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class CelerySettings(BaseSettings):
    CELERY_BROKER_URL: str = Field(validation_alias="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(validation_alias="CELERY_RESULT_BACKEND")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
