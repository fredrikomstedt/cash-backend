from functools import lru_cache
from passlib.context import CryptContext


@lru_cache()
def get_crypt_context() -> CryptContext:
    return CryptContext(schemes=['bcrypt'], deprecated=["auto"])
