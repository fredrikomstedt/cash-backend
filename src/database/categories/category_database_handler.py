from sqlmodel import Session, select

from src.common.exceptions import ObjectNotFoundError
from src.database.categories.category import Category
from src.database.categories.i_category_database_handler import ICategoryDatabaseHandler
from src.database.users.user import User


class CategoryDatabaseHandler(ICategoryDatabaseHandler):
    def create_category(self, session: Session, user: User, name: str) -> Category:
        statement = select(Category).where(Category.user == user, Category.name == name)
        results = session.exec(statement)
        db_category = results.first()
        if db_category:
            raise ValueError("Category with that name already exists")

        category = Category(name=name, user=user)
        session.add(category)
        return category

    def get_categories(self, session: Session, user: User) -> list[Category]:
        statement = select(Category).where(Category.user == user)
        results = session.exec(statement)
        categories = results.all()

        return categories

    def delete_category(self, session: Session, user: User, name: str) -> None:
        statement = select(Category).where(Category.user == user, Category.name == name)
        results = session.exec(statement)
        category = results.first()
        if not category:
            raise ObjectNotFoundError("No category with that name exists.")

        session.delete(category)
