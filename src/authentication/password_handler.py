from injector import inject
from passlib.context import CryptContext

from src.authentication.i_password_handler import IPasswordHandler


class PasswordHandler(IPasswordHandler):
    @inject
    def __init__(self, crypt_context: CryptContext):
        self.__context = crypt_context

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.__context.verify(plain_password, hashed_password)

    def hash_password(self, plain_password: str) -> str:
        return self.__context.hash(plain_password)
