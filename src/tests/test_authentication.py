from unittest import TestCase
from unittest.mock import create_autospec

from injector import Injector, singleton

from src.authentication.authentication import Authentication
from src.authentication.i_password_handler import IPasswordHandler
from src.common.exceptions import ObjectNotFoundError
from src.common.i_jwt_encoder import IJwtEncoder
from src.database.users.i_user_manager import IUserManager
from src.database.users.user import User


class TestAuthentication(TestCase):
    def setUp(self):
        self.__password_handler = create_autospec(IPasswordHandler)
        self.__jwt_encoder = create_autospec(IJwtEncoder)
        self.__user_manager = create_autospec(IUserManager)

        self.__injector = Injector()
        self.__injector.binder.bind(
            IPasswordHandler, to=self.__password_handler, scope=singleton)
        self.__injector.binder.bind(
            IJwtEncoder, to=self.__jwt_encoder, scope=singleton)
        self.__injector.binder.bind(
            IUserManager, to=self.__user_manager, scope=singleton)

    def test_authenticate_user_raises_on_no_user_information(self):
        self.__jwt_encoder.decode.return_value = {}

        authentication = self.__injector.get(Authentication)

        with self.assertRaises(ValueError):
            authentication.authenticate_user("token")

    def test_authenticate_user_raises_on_user_not_existing(self):
        self.__jwt_encoder.decode.return_value = {"sub": "test@email.com"}
        self.__user_manager.get_user_with_email.return_value = None

        authentication = self.__injector.get(Authentication)

        with self.assertRaises(ObjectNotFoundError):
            authentication.authenticate_user("token")

    def test_authenticate_user_returns_user(self):
        token = "token"
        test_email = "test@email.com"
        user = User(email=test_email)
        self.__jwt_encoder.decode.return_value = {"sub": test_email}
        self.__user_manager.get_user_with_email.return_value = user

        authentication = self.__injector.get(Authentication)
        returned_user = authentication.authenticate_user(token)

        self.__jwt_encoder.decode.assert_called_once_with(token)
        self.__user_manager.get_user_with_email.assert_called_once_with(
            test_email)
        self.assertEqual(returned_user, user)

    def test_login_user_raises_on_user_not_existing(self):
        self.__user_manager.get_user_with_email.return_value = None

        authentication = self.__injector.get(Authentication)

        with self.assertRaises(ObjectNotFoundError):
            authentication.login_user("test@email.com", "password")

    def test_login_user_raises_on_invalid_password(self):
        self.__user_manager.get_user_with_email.return_value = User(
            email="test@email.com")
        self.__password_handler.verify_password.return_value = False

        authentication = self.__injector.get(Authentication)

        with self.assertRaises(ValueError):
            authentication.login_user("test@email.com", "password")

    def test_login_user_returns_encoded_token(self):
        test_email = "test@email.com"
        password = "password"
        encoded_token = "encoded-token"
        self.__user_manager.get_user_with_email.return_value = User(
            email=test_email)
        self.__password_handler.verify_password.return_value = True
        self.__jwt_encoder.encode.return_value = encoded_token

        authentication = self.__injector.get(Authentication)
        token = authentication.login_user(test_email, password)

        self.assertEqual(token, encoded_token)
        self.__jwt_encoder.encode.assert_called_once()

