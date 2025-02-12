from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 15
    database_url: str
    crypto_secret: str
    log_level: str = "INFO"
    root_user_email: str
    root_user_password: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


settings = Settings()


class JWTSettings(BaseModel):
    authjwt_secret_key: str = settings.jwt_secret_key
    authjwt_algorithm: str = settings.jwt_algorithm
    access_token_expire_minutes: int = settings.jwt_access_token_expire_minutes
    refresh_token_expire_days: int = settings.jwt_refresh_token_expire_days


jwt_settings = JWTSettings()
