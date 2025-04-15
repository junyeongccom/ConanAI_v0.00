from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
DATABASE_URL = settings.DATABASE_URL
