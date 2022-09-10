from calendar import c
from passlib.context import CryptContext

from .i_password_handler import IPasswordHandler


class PasswordHandler(IPasswordHandler):
    def __init__(self):
        self.__context = CryptContext(schemes=['bcrypt'], deprecated=["auto"])

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.__context.verify(plain_password, hashed_password)

    def hash_password(self, plain_password: str) -> str:
        return self.__context.hash(plain_password)
