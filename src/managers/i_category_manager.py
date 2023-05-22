from abc import ABC, abstractmethod

from src.database.categories.category import Category, CategoryCreate
from src.database.users.user import User


class ICategoryManager(ABC):
    @abstractmethod
    def create_category(self, user: User, data: CategoryCreate) -> Category:
        """Creates a new category for the given user in the database.
        Raises if the category already exists for the user.

        Returns the newly created category."""

    @abstractmethod
    def get_categories(self, user: User) -> list[Category]:
        """Fetches a user's categories."""

    @abstractmethod
    def delete_category(self, user: User, name: str) -> None:
        """Deletes a category for the given user in the database.
        Raises if the category does not exist for the user."""
