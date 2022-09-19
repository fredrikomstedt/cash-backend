from database.users.user import User
from fastapi_injector import Injected

from .i_authentication import IAuthentication
from .i_password_handler import IPasswordHandler


class Authentication(IAuthentication):
    def __init__(self, password_handler: IPasswordHandler = Injected(IPasswordHandler)):
        self.__password_handler = password_handler

    def login_user(self, username: str, password: str) -> str:
        pass

    def authenticate_user(self, token: str) -> User:
        pass
