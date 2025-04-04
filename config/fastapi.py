from enum import Enum

from pydantic_settings import BaseSettings


class AppEnv(Enum):
    """
    Defines application environments. Default env is development
    Member values must map to the Environments Enum in config.py
    """

    LOCAL: str = "local"
    DEV: str = "development"
    STAGING: str = "staging"
    PROD: str = "production"


class Settings(BaseSettings):
    # Server Configs
    APP_ENV: AppEnv = "local"
    SERVER_NAME: str = "Rejuven AI"
    # LOG_FILE: str = "/var/log/rejuvenAI.log"

    # AWS & S3 Configs
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    S3_AWS_REGION: str = "us-east-2"
    S3_BUCKET_NAME: str = "rejuvenai-staging"

    # JWT Configs
    JWT_PUBLIC_KEY: str = ""
    JWT_PRIVATE_KEY: str = ""
    JWT_SIGNATURE_ALGORITHM: str = "RS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 45


app_settings = Settings()
