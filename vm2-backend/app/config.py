from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    MYSQL_HOST: str = "localhost"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "test"
    
    # Gemini API
    GEMINI_API_KEY: Optional[str] = None
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # rsync
    RSYNC_HOST: str = "vm3-storage"
    RSYNC_PORT: int = 873
    RSYNC_USER: str = "app_user"
    RSYNC_PASSWORD: Optional[str] = None
    RSYNC_MODULE: str = "company_data"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()