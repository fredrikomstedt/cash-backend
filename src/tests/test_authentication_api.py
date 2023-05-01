from unittest import TestCase
from unittest.mock import create_autospec

from fastapi import status
from fastapi.testclient import TestClient
from injector import Injector, singleton

from src.authentication.i_authentication import IAuthentication
from src.authentication.i_password_handler import IPasswordHandler
from src.common.exceptions import ObjectNotFoundError
from src.database.users.user import User
from src.main import create_app
from src.managers.i_user_manager import IUserManager


class TestApi(TestCase):
    def setUp(self):
        self.__authentication = create_autospec(IAuthentication)
        self.__password_handler = create_autospec(IPasswordHandler)
        self.__user_manager = create_autospec(IUserManager)

        self.__injector = Injector()
        self.__injector.binder.bind(
            IAuthentication, to=self.__authentication, scope=singleton
        )
        self.__injector.binder.bind(
            IPasswordHandler, to=self.__password_handler, scope=singleton
        )
        self.__injector.binder.bind(
            IUserManager, to=self.__user_manager, scope=singleton
        )

        app = create_app(self.__injector)
        self.__client = TestClient(app)

    def test_login_for_access_token_unauthorized(self):
        self.__authentication.login_user.side_effect = ValueError()

        response = self.__client.post(
            "/auth/token", data={"username": "bla", "password": "bla"}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_for_access_token_returns_token_and_type(self):
        token = "i-am-a-token"
        username = "bla"
        password = "blabla"
        self.__authentication.login_user.return_value = token

        response = self.__client.post(
            "/auth/token", data={"username": username, "password": password}
        )

        self.__authentication.login_user.assert_called_once_with(username, password)
        token_data = response.json()
        self.assertIn("token_type", token_data)
        self.assertEqual("bearer", token_data["token_type"])
        self.assertIn("access_token", token_data)
        self.assertEqual(token, token_data["access_token"])

    def test_create_user_bad_request(self):
        self.__user_manager.create_user.side_effect = ValueError()

        response = self.__client.post(
            "/auth/create-user",
            json={"email": "fredrik@omstedt.com", "password": "password"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_returns_user_read(self):
        email = "fredrik@omstedt.com"
        first_name = "Fredrik"
        last_name = "Omstedt"
        self.__user_manager.create_user.return_value = User(
            email=email, first_name=first_name, last_name=last_name
        )

        response = self.__client.post(
            "/auth/create-user", json={"email": email, "password": "password"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = response.json()
        self.assertNotIn("hashed_password", user)
        self.assertEqual(first_name, user["first_name"])
        self.assertEqual(last_name, user["last_name"])
        self.assertEqual(email, user["email"])

    def test_get_user_unauthorized(self):
        response = self.__client.get("/auth/get-user")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_success(self):
        email = "fredrik@omstedt.com"
        first_name = "Fredrik"
        last_name = "Omstedt"
        self.__authentication.authenticate_user.return_value = User(
            email=email, first_name=first_name, last_name=last_name
        )

        response = self.__client.get(
            "/auth/get-user", headers={"Authorization": "Bearer blabla"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = response.json()
        self.assertNotIn("hashed_password", user)
        self.assertEqual(first_name, user["first_name"])
        self.assertEqual(last_name, user["last_name"])
        self.assertEqual(email, user["email"])

    def test_update_user_unauthorized(self):
        response = self.__client.patch("/auth/update-user", json={})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_not_found(self):
        self.__user_manager.update_user.side_effect = ObjectNotFoundError()

        response = self.__client.patch(
            "/auth/update-user", json={}, headers={"Authorization": "Bearer blabla"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_returns_user_read(self):
        email = "fredrik@omstedt.com"
        first_name = "Fredrik"
        last_name = "Omstedt"
        self.__user_manager.update_user.return_value = User(
            email=email, first_name=first_name, last_name=last_name
        )

        response = self.__client.patch(
            "/auth/update-user", json={}, headers={"Authorization": "Bearer blabla"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = response.json()
        self.assertNotIn("hashed_password", user)
        self.assertEqual(first_name, user["first_name"])
        self.assertEqual(last_name, user["last_name"])
        self.assertEqual(email, user["email"])

    def test_update_user_password_unauthorized(self):
        response = self.__client.patch("/auth/update-user-password", json={})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_password_wrong_password(self):
        self.__password_handler.verify_password.return_value = False

        response = self.__client.patch(
            "/auth/update-user-password",
            json={"old_password": "bla", "new_password": "blabla"},
            headers={"Authorization": "Bearer blabla"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_password_not_found(self):
        self.__password_handler.verify_password.return_value = True
        self.__user_manager.update_user_password.side_effect = ObjectNotFoundError()

        response = self.__client.patch(
            "/auth/update-user-password",
            json={"old_password": "bla", "new_password": "blabla"},
            headers={"Authorization": "Bearer blabla"},
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_password_returns_user_read(self):
        email = "fredrik@omstedt.com"
        first_name = "Fredrik"
        last_name = "Omstedt"
        self.__user_manager.update_user_password.return_value = User(
            email=email, first_name=first_name, last_name=last_name
        )

        self.__password_handler.verify_password.return_value = True
        response = self.__client.patch(
            "/auth/update-user-password",
            json={"old_password": "bla", "new_password": "blabla"},
            headers={"Authorization": "Bearer blabla"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = response.json()
        self.assertNotIn("hashed_password", user)
        self.assertEqual(first_name, user["first_name"])
        self.assertEqual(last_name, user["last_name"])
        self.assertEqual(email, user["email"])

    def test_delete_user_unauthorized(self):
        response = self.__client.delete("/auth/delete-user")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_not_found(self):
        self.__user_manager.delete_user.side_effect = ObjectNotFoundError()

        response = self.__client.delete(
            "/auth/delete-user", headers={"Authorization": "Bearer blabla"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user_success(self):
        response = self.__client.delete(
            "/auth/delete-user", headers={"Authorization": "Bearer blabla"}
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.__user_manager.delete_user.assert_called_once()
