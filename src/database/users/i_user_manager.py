from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import EmailStr

from .user import User, UserCreate, UserUpdate


class IUserManager(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate) -> User:
        """Creates a new user in the database. Raises if the user
           already exists. 

           Returns the newly created user."""

    @abstractmethod
    def get_user(self, id: UUID) -> User:
        """Fetches a user with the given ID. Raises an 
           exception if the user does not exist."""

    @abstractmethod
    def get_user_with_email(self, email: EmailStr) -> User:
        """Fetches a user with the given email. Raises an 
           exception if the user does not exist."""

    @abstractmethod
    def update_user(self, id: UUID, user: UserUpdate) -> User:
        """Updates the user with the provided user values.
           Raises an exception if the user does not exist."""
