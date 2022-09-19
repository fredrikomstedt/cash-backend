from fastapi import Depends
from passlib.context import CryptContext

from .dependencies import get_crypt_context


class PasswordHandler:
    def __init__(self, crypt_context: CryptContext = Depends(get_crypt_context)):
        self.__context = crypt_context

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies that the plain_password matches the hashed_password."""
        return self.__context.verify(plain_password, hashed_password)

    def hash_password(self, plain_password: str) -> str:
        """Hashes the supplied password and returns it."""
        return self.__context.hash(plain_password)
