from uuid import UUID

from database.i_database import IDatabase
from database.users.user import User, UserCreate, UserUpdate
from injector import inject
from pydantic import EmailStr
from sqlmodel import select

from .i_user_manager import IUserManager


class UserManager(IUserManager):
    @inject
    def __init__(self, database: IDatabase):
        self.__database = database

    def create_user(self, user: UserCreate) -> User:
        with self.__database.get_session() as session:
            db_user = User.from_orm(user)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

    def get_user(self, id: UUID) -> User:
        with self.__database.get_session() as session:
            user = session.get(User, id)
            if not user:
                raise ValueError("No user with that ID exists.")

    def get_user_with_email(self, email: EmailStr) -> User:
        with self.__database.get_session() as session:
            statement = select(User).where(User.email == email)
            results = session.exec(statement)
            user = results.first()
            if not user:
                raise ValueError("No user with that email exists.")
            return user

    def update_user(self, id: UUID, user: UserUpdate) -> User:
        with self.__database.get_session() as session:
            db_user = session.get(User, id)
            if not db_user:
                raise ValueError("No user with that ID exists.")
            user_data = user.dict(exclude_unset=True)
            for key, value in user_data.items():
                setattr(db_user, key, value)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user
