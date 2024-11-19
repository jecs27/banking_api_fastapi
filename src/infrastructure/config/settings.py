from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "banking-api"
    
    # SECURITY
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    BACKEND_CORS_ORIGINS: List[str] = [
        url.strip() for url in 
        os.getenv(
            "BACKEND_CORS_ORIGINS",
            "http://localhost:8000,http://localhost:3000"
        ).split(",")
    ]

    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/banking_db")
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    # Email settings
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT"))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME")

    class Config:
        case_sensitive = True

settings = Settings()