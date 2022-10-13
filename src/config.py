# src/config.py

from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
  env_name: str = "Local"
  port: int = 8080

  class Config:
    env_file = ".env"

@lru_cache
def get_settings() -> Settings:
  settings = Settings()
  print(f"Loading settings for: {settings.env_name}", f"on port: {settings.port}")
  return settings
