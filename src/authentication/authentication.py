from base64 import encode
from datetime import datetime, timedelta

from injector import inject
from pydantic import EmailStr

from src.authentication.i_authentication import IAuthentication
from src.authentication.i_password_handler import IPasswordHandler
from src.common.exceptions import ObjectNotFoundError
from src.common.i_jwt_encoder import IJwtEncoder
from src.common.settings import Settings
from src.database.users.user import User
from src.managers.i_user_manager import IUserManager


class Authentication(IAuthentication):
    @inject
    def __init__(
        self,
        password_handler: IPasswordHandler,
        jwt_encoder: IJwtEncoder,
        user_manager: IUserManager,
        settings: Settings,
    ):
        self.__password_handler = password_handler
        self.__jwt_encoder = jwt_encoder
        self.__user_manager = user_manager
        self.__settings = settings

    def login_user(self, email: str, password: str) -> str:
        user = self.__validate_email_and_password(email, password)
        access_token = self.__create_access_token({"sub": user.email})
        return access_token

    def authenticate_user(self, token: str) -> User:
        payload = self.__jwt_encoder.decode(token)
        email: EmailStr = payload.get("sub")
        if email is None:
            raise ValueError("Token contains no user information.")
        user = self.__user_manager.get_user_with_email(email)
        if user is None:
            raise ObjectNotFoundError("User does not exist.")
        return user

    def __validate_email_and_password(self, email: str, password: str) -> User:
        user = self.__user_manager.get_user_with_email(email)
        if user is None:
            raise ObjectNotFoundError("User does not exist.")
        if not self.__password_handler.verify_password(password, user.hashed_password):
            raise ValueError("Incorrect password.")
        return user

    def __create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            hours=self.__settings.access_token_expire_hours
        )
        to_encode.update({"exp": expire})
        encoded_jwt = self.__jwt_encoder.encode(to_encode)
        return encoded_jwt
