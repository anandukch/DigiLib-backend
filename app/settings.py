from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str
    MONGO_INITDB_DATABASE=str

    class Config:
        env_file = "./.env"


settings = Settings()
