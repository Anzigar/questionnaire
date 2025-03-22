from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = ['*']  
    APP_SECRET_KEY: Optional[str] = None
    HOST: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()