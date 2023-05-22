from injector import inject

from src.database.categories.category import Category, CategoryCreate
from src.database.categories.i_category_database_handler import ICategoryDatabaseHandler
from src.database.i_database import IDatabase
from src.database.users.user import User
from src.managers.i_category_manager import ICategoryManager


class CategoryManager(ICategoryManager):
    @inject
    def __init__(self, database: IDatabase, category_handler: ICategoryDatabaseHandler):
        self.__database = database
        self.__category_handler = category_handler

    def create_category(self, user: User, data: CategoryCreate) -> Category:
        with self.__database.get_session() as session:
            category = self.__category_handler.create_category(session, user, data.name)
            session.commit()
            session.refresh(category)
            return category

    def get_categories(self, user: User) -> list[Category]:
        with self.__database.get_session() as session:
            categories = self.__category_handler.get_categories(session, user)
            return categories

    def delete_category(self, user: User, name: str) -> None:
        with self.__database.get_session() as session:
            self.__category_handler.delete_category(session, user, name)
