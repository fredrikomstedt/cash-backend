from injector import inject
from pydantic import EmailStr
from sqlmodel import select

from src.authentication.i_password_handler import IPasswordHandler
from src.common.exceptions import ObjectNotFoundError
from src.database.i_database import IDatabase
from src.database.users.user import User, UserCreate, UserUpdate
from src.managers.i_user_manager import IUserManager


class UserManager(IUserManager):
    @inject
    def __init__(self, database: IDatabase, password_handler: IPasswordHandler):
        self.__database = database
        self.__password_handler = password_handler

    def create_user(self, user: UserCreate) -> User:
        if self.get_user_with_email(user.email):
            raise ValueError("User with that email already exists")

        hashed_password = self.__password_handler.hash_password(user.password)
        db_user = User.from_orm(user)
        db_user.hashed_password = hashed_password

        with self.__database.get_session() as session:
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

    def get_user(self, id: str) -> User | None:
        with self.__database.get_session() as session:
            user = session.get(User, id)
            return user

    def get_user_with_email(self, email: EmailStr) -> User | None:
        with self.__database.get_session() as session:
            statement = select(User).where(User.email == email)
            results = session.exec(statement)
            user = results.first()
            return user

    def update_user(self, id: str, user: UserUpdate) -> User:
        with self.__database.get_session() as session:
            db_user = session.get(User, id)
            if not db_user:
                raise ObjectNotFoundError("No user with that ID exists.")
            user_data = user.dict(exclude_unset=True)
            for key, value in user_data.items():
                setattr(db_user, key, value)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

    def update_user_password(self, id: str, password: str) -> User:
        with self.__database.get_session() as session:
            db_user = session.get(User, id)
            if not db_user:
                raise ObjectNotFoundError("No user with that ID exists.")
            hashed_password = self.__password_handler.hash_password(password)
            db_user.hashed_password = hashed_password
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

    def delete_user(self, id: str) -> None:
        with self.__database.get_session() as session:
            db_user = session.get(User, id)
            if not db_user:
                raise ObjectNotFoundError("No user with that ID exists.")

            session.delete(db_user)
            session.commit()
