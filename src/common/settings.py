from pydantic import BaseSettings


class Settings(BaseSettings):
    authentication_secret: str = ''
    database_url: str = ''

    class Config:
        env_file = '.env'
