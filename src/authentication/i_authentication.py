from abc import ABC, abstractmethod

from database.users.user import User


class IAuthentication(ABC):
    @abstractmethod
    def login_user(self, email: str, password: str) -> str:
        """Logs in a user with the supplied email and password,
           assuming the user exists and is verified.

           Returns a token for authenticated requests."""

    @abstractmethod
    def authenticate_user(self, token: str) -> User:
        """Authenticates the supplied token and returns
           the user associated with it."""
