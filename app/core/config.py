from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/streetwear_market"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

    @property
    def is_debug(self) -> bool:
        return self.DEBUG or self.ENVIRONMENT == "development"


settings = Settings()
