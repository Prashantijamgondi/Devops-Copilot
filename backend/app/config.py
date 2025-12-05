from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "DevOps Co-Pilot"
    DEBUG: bool = False
    API_VERSION: str = "v1"
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # AI Services
    #TOGETHER_API_KEY: str
    #OUMI_MODEL: str = "meta-llama/Llama-3.2-3B-Instruct-Turbo"
    AI_PROVIDER: str = "groq"  # or "together"
    GROQ_API_KEY: str = ""
    TOGETHER_API_KEY: str = ""
    OUMI_MODEL: str = "llama-3.1-70b-versatile"
    
    # Kestra
    KESTRA_URL: str
    KESTRA_API_KEY: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: str = "*"
    
    # Monitoring
    WEBHOOK_SECRET: str
    SLACK_WEBHOOK_URL: str = ""
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # NEW ADDED THIS LINE - Ignore extra env variables

@lru_cache()
def get_settings():
    return Settings()
