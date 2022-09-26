from unittest import TestCase
from unittest.mock import create_autospec

from authentication.current_user import get_current_user
from authentication.i_authentication import IAuthentication
from common.exceptions import ObjectNotFoundError
from database.users.user import User
from fastapi import HTTPException


class TestCurrentUser(TestCase):
    def setUp(self):
        self.__authentication = create_autospec(IAuthentication)

    def test_get_current_user_returns_authenticated_user(self):
        user = User(email="bla@bla.com")
        token = "Blabla"
        self.__authentication.authenticate_user.return_value = user
        returned_user = get_current_user(token, self.__authentication)
        self.assertEqual(user, returned_user)
        self.__authentication.authenticate_user.assert_called_once_with(token)

    def test_get_current_user_raises_bad_request(self):
        self.__authentication.authenticate_user.side_effect = ObjectNotFoundError()

        with self.assertRaises(HTTPException):
            get_current_user("Blabla", self.__authentication)
