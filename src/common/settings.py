from pydantic import BaseSettings

from src.common.utils import get_project_path


class Settings(BaseSettings):
    authentication_secret: str = ''
    database_url: str = ''
    access_token_expire_hours: int = 4

    class Config:
        env_file = get_project_path('.env')
