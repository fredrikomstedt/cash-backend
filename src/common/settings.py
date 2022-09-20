from pydantic import BaseSettings


class Settings(BaseSettings):
    authentication_secret: str = ''
    database_url: str = ''
    access_token_expire_hours: int = 4

    class Config:
        env_file = '.env'
