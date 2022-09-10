from pydantic import BaseSettings


class Settings(BaseSettings):
    authentication_secret: str = ''

    class Config:
        env_file = '.env'
