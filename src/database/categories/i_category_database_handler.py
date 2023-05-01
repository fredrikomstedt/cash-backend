from abc import ABC, abstractmethod

from sqlmodel import Session

from src.database.categories.category import Category
from src.database.users.user import User


class ICategoryDatabaseHandler(ABC):
    @abstractmethod
    def create_category(self, session: Session, user: User, name: str) -> Category:
        """Creates a category with the given name for the given user."""

    @abstractmethod
    def get_categories(self, session: Session, user: User) -> list[Category]:
        """Retrieves a user's categories."""

    @abstractmethod
    def delete_category(self, session: Session, user: User, name: str) -> None:
        """Delete a user's category with the given name."""
