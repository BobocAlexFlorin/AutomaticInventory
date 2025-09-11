import os
from pydantic import BaseSettings


class Settings(BaseSettings):
database_url: str = os.getenv("DATABASE_URL")
snipeit_url: str | None = os.getenv("SNIPEIT_URL")
snipeit_token: str | None = os.getenv("SNIPEIT_TOKEN")


settings = Settings()