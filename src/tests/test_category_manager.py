from unittest import TestCase
from unittest.mock import ANY, create_autospec

from injector import singleton
from sqlmodel import select

from src.common.exceptions import ObjectNotFoundError
from src.database.categories.category import Category, CategoryCreate
from src.database.categories.i_category_database_handler import ICategoryDatabaseHandler
from src.database.i_database import IDatabase
from src.database.users.user import User, UserCreate, UserUpdate
from src.managers.category_manager import CategoryManager
from src.managers.user_manager import UserManager
from src.multi_injector import MultiInjector


class TestUserManager(TestCase):
    def setUp(self):
        self.__database = create_autospec(IDatabase)
        self.__category_handler = create_autospec(ICategoryDatabaseHandler)
        self.__user = User(email="fredrik@omstedt.com")

        self.__injector = MultiInjector()
        self.__injector.binder.bind(IDatabase, to=self.__database, scope=singleton)
        self.__injector.binder.bind(
            ICategoryDatabaseHandler, to=self.__category_handler, scope=singleton
        )

    def test_create_category(self):
        manager = self.__injector.get(CategoryManager)
        data = CategoryCreate(name="Food")

        manager.create_category(self.__user, data)

        self.__database.get_session.assert_called_once()
        self.__category_handler.create_category.assert_called_once_with(
            ANY, self.__user, data.name
        )

    def test_get_categories(self):
        manager = self.__injector.get(CategoryManager)
        categories = [Category(name="Food"), Category(name="Car")]
        self.__category_handler.get_categories.return_value = categories

        returned_categories = manager.get_categories(self.__user)

        self.__database.get_session.assert_called_once()
        self.__category_handler.get_categories.assert_called_once_with(ANY, self.__user)
        self.assertEqual(categories, returned_categories)

    def test_delete_category(self):
        manager = self.__injector.get(CategoryManager)
        name = "Food"

        manager.delete_category(self.__user, name)

        self.__database.get_session.assert_called_once()
        self.__category_handler.delete_category.assert_called_once_with(
            ANY, self.__user, name
        )
