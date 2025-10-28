"""Core configuration settings"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "AI Visibility Tool"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    allowed_origins: List[str] = ["*"]
    
    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
