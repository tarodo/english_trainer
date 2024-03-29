import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str = "HS256"
    DB_URL: str = "sqlite:///db_test.db"

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    EMAIL_TEST_USER: str = "test@test.com"

    class Config:
        case_sensitive = True


settings = Settings()
