from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str = "sqlite:///./mcp.db"

    class Config:
        env_file = ".env"

settings = Settings()
