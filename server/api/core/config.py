from dotenv import dotenv_values
from pydantic import BaseSettings

config = dotenv_values(".env")


class Settings(BaseSettings):
    # TODO change secret key to environment variable
    SECRET_KEY: str = "s3cr3t"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    PROJECT_NAME: str = "Sales Automation"

    class Config:
        case_sensitive = True


settings = Settings()
