from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PORT: int = 8000
    ALLOWED_ORIGINS: str

    class Config:
        env_file = ".env"

        case_sensitive = True


settings = Settings()