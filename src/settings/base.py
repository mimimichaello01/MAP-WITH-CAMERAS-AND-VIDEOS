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

# class AuthSettings(BaseSettings):
#     SECRET_KEY: str = Field(default="supersecretkey", validation_alias="SECRET_KEY")
#     ALGORITHM: str = Field(default="HS256", validation_alias="ALGORITHM")
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15)
#     REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

#     model_config = SettingsConfigDict(env_file=".env", extra="ignore")
