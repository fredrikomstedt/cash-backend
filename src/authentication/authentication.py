from common.i_jwt_encoder import IJwtEncoder
from database.users.user import User
from injector import inject

from .i_authentication import IAuthentication
from .i_password_handler import IPasswordHandler


class Authentication(IAuthentication):
    @inject
    def __init__(self, password_handler: IPasswordHandler, jwt_encoder: IJwtEncoder):
        self.__password_handler = password_handler
        self.__jwt_encoder = jwt_encoder

    def login_user(self, username: str, password: str) -> str:
        pass

    def authenticate_user(self, token: str) -> User:
        pass
