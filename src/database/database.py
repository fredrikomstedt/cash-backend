from injector import inject
from sqlmodel import Session, SQLModel, create_engine

from src.database.i_database import IDatabase
from src.database.i_database_deleter import IDatabaseDeleter
from src.common.settings import Settings


class Database(IDatabase, IDatabaseDeleter):
    @inject
    def __init__(self, settings: Settings):
        if settings.database_url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}
            self.__engine = create_engine(
                settings.database_url, connect_args=connect_args
            )
        else:
            self.__engine = create_engine(settings.database_url)

    def create_database(self) -> None:
        SQLModel.metadata.create_all(self.__engine)

    def delete_database(self) -> None:
        SQLModel.metadata.drop_all(self.__engine)

    def get_session(self) -> Session:
        return Session(self.__engine)