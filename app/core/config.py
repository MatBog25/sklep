from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Clothing Store API"
    environment: str = "development"
    debug: bool = True
    mongodb_uri: str = "mongodb://shop_user:shop_password@localhost:27017/clothing_store?authSource=admin"
    mongodb_db_name: str = "clothing_store"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

