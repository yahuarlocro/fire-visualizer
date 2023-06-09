"""Configuration File
"""
import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_user: str  
    postgres_pw: str  
    postgres_host: str  
    postgres_db: str  
    redis_host: str
    redis_port: int

    class Config:
        env_file = ".env"

settings = Settings()
