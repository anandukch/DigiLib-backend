
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str
    # POSTGRES_HOST: str
    # POSTGRES_PORT: int
    
    MONGO_URL: str

    # JWT
    # JWT_SECRET_KEY: str
    # JWT_ALGORITHM: str
    # JWT_EXPIRE_TIME: int

    # CORS
    # CORS_ORIGINS: str

    # Log
    # LOG_LEVEL: str

    class Config:
        env_file = "./.env"
        
settings = Settings()
  