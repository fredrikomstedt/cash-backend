from unittest import TestCase

from sqlmodel import select

from src.common.exceptions import ObjectNotFoundError
from src.database.categories.category import Category
from src.database.categories.category_database_handler import CategoryDatabaseHandler
from src.database.i_database import IDatabase
from src.database.i_database_deleter import IDatabaseDeleter
from src.database.users.user import User
from src.tests.test_utils import create_injector_with_database


class TestCategoryDatabaseHandler(TestCase):
    def setUp(self):
        self.__injector = create_injector_with_database()

        database = self.__injector.get(IDatabase)
        database.create_database()
        self.__user = User(email="fredrik@omstedt.com")
        database = self.__injector.get(IDatabase)
        with database.get_session() as session:
            session.add(self.__user)
            session.commit()
            session.refresh(self.__user)

    def tearDown(self) -> None:
        database_deleter = self.__injector.get(IDatabaseDeleter)
        database_deleter.delete_database()

    def test_create_category_raises_if_already_exists(self):
        name = "Car"
        database = self.__injector.get(IDatabase)
        with database.get_session() as session:
            category = Category(name=name, user=self.__user)
            session.add(category)
            session.commit()
            session.refresh(category)

        handler = self.__injector.get(CategoryDatabaseHandler)
        with self.assertRaises(ValueError):
            with database.get_session() as session:
                handler.create_category(session, self.__user, name)

    def test_create_category_creates_category(self):
        name = "Car"
        database = self.__injector.get(IDatabase)
        handler = self.__injector.get(CategoryDatabaseHandler)
        with database.get_session() as session:
            category = handler.create_category(session, self.__user, name)
            session.commit()
            session.refresh(category)

        with database.get_session() as session:
            db_category = session.get(Category, name)
            self.assertEqual(db_category.name, category.name)
            self.assertEqual(db_category.user, category.user)

    def test_get_categories_returns_empty_if_no_categories(self):
        database = self.__injector.get(IDatabase)
        handler = self.__injector.get(CategoryDatabaseHandler)
        with database.get_session() as session:
            categories = handler.get_categories(session, self.__user)
            self.assertEqual(len(categories), 0)

    def test_get_categories_returns_categories(self):
        database = self.__injector.get(IDatabase)
        handler = self.__injector.get(CategoryDatabaseHandler)
        with database.get_session() as session:
            category = Category(name="Car", user=self.__user)
            category2 = Category(name="Savings", user=self.__user)
            session.add(category)
            session.add(category2)
            session.commit()
            session.refresh(category)
            session.refresh(category2)

        with database.get_session() as session:
            categories = handler.get_categories(session, self.__user)
            self.assertEqual(len(categories), 2)

    def test_delete_category_raises_if_category_not_existing(self):
        database = self.__injector.get(IDatabase)
        handler = self.__injector.get(CategoryDatabaseHandler)
        with self.assertRaises(ObjectNotFoundError):
            with database.get_session() as session:
                handler.delete_category(session, self.__user, "invalid-category")

    def test_delete_category_deletes_category(self):
        name = "Car"
        database = self.__injector.get(IDatabase)
        with database.get_session() as session:
            category = Category(name=name, user=self.__user)
            session.add(category)
            session.commit()
            session.refresh(category)

        handler = self.__injector.get(CategoryDatabaseHandler)
        with database.get_session() as session:
            handler.delete_category(session, self.__user, name)
            session.commit()

        with database.get_session() as session:
            statement = select(Category).where(Category.name == name)
            results = session.exec(statement)
            db_user = results.first()
            self.assertIsNone(db_user)
