from abc import ABC, abstractmethod


class IPasswordHandler(ABC):
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies that the plain_password matches the hashed_password."""

    @abstractmethod
    def hash_password(self, plain_password: str) -> str:
        """Hashes the supplied password and returns it."""
