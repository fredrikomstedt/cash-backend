from unittest import TestCase
from unittest.mock import create_autospec

from injector import singleton
from sqlmodel import select

from src.authentication.i_password_handler import IPasswordHandler
from src.database.i_database import IDatabase
from src.database.i_database_deleter import IDatabaseDeleter
from src.database.users.user import User, UserCreate
from src.database.users.user_manager import UserManager
from src.tests.test_utils import create_injector_with_database


class TestUserManager(TestCase):
    def setUp(self):
        self.__password_handler = create_autospec(IPasswordHandler)
        self.__injector = create_injector_with_database()
        self.__injector.binder.bind(
            IPasswordHandler, to=self.__password_handler, scope=singleton)

        database = self.__injector.get(IDatabase)
        database.create_database()

    def tearDown(self) -> None:
        database_deleter = self.__injector.get(IDatabaseDeleter)
        database_deleter.delete_database()

    def test_create_user_raises_if_user_with_email_exists(self):
        email = "fredrik@omstedt.com"
        database = self.__injector.get(IDatabase)
        with database.get_session() as session:
            user = User(email=email)
            session.add(user)
            session.commit()
            session.refresh(user)

        manager = self.__injector.get(UserManager)
        with self.assertRaises(ValueError):
            manager.create_user(UserCreate(email=email, password="password"))

    def test_create_user_stores_with_hashed_password(self):
        email = "fredrik@omstedt.com"
        password = "password"
        hashed_password = "420password"
        self.__password_handler.hash_password.return_value = hashed_password

        manager = self.__injector.get(UserManager)
        user = manager.create_user(UserCreate(email=email, password=password))

        self.__password_handler.hash_password.assert_called_once_with(password)

        database = self.__injector.get(IDatabase)
        with database.get_session() as session:
            statement = select(User).where(User.id == user.id)
            results = session.exec(statement)
            db_user = results.first()
            self.assertIsNotNone(db_user)
            self.assertEqual(hashed_password, db_user.hashed_password)
            self.assertEqual(email, db_user.email)

    def test_get_user_returns_none_if_user_not_existing(self):
        manager = self.__injector.get(UserManager)
        self.assertIsNone(manager.get_user("invalid-id"))

    def test_get_user_returns_user(self):
        email = "fredrik@omstedt.com"
        database = self.__injector.get(IDatabase)
        with database.get_session() as session:
            user = User(email=email)
            session.add(user)
            session.commit()
            session.refresh(user)
            user_id = user.id

        manager = self.__injector.get(UserManager)
        db_user = manager.get_user(user_id)
        self.assertEqual(db_user.email, email)

    def test_get_user_with_email_returns_none_if_user_not_existing(self):
        manager = self.__injector.get(UserManager)
        self.assertIsNone(manager.get_user_with_email("invalid-email"))

    def test_get_user_with_email_returns_user(self):
        email = "fredrik@omstedt.com"
        database = self.__injector.get(IDatabase)
        with database.get_session() as session:
            user = User(email=email)
            session.add(user)
            session.commit()
            session.refresh(user)

        manager = self.__injector.get(UserManager)
        db_user = manager.get_user_with_email(email)
        self.assertEqual(db_user.email, email)
