"""
Application Configuration

Configuration management using Pydantic BaseSettings.
Loads settings from environment variables and .env file.
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""

    # Project
    PROJECT_NAME: str = "REST API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/dbname",
        description="PostgreSQL database URL",
    )

    # Security
    SECRET_KEY: str = Field(..., description="Secret key for JWT token generation (REQUIRED)")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Environment
    ENVIRONMENT: str = Field(
        default="development", description="Environment (development, staging, production)"
    )
    DEBUG: bool = Field(default=True, description="Debug mode")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create settings instance
settings = Settings()
