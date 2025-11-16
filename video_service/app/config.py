from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JITSI_DOMAIN: str = "meet.jit.si"
    JITSI_APP_ID: str = "your-jitsi-app-id"
    
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
    ]
    
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 2
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
