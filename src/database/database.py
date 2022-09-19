from injector import inject
from settings import Settings
from sqlmodel import Session, SQLModel, create_engine

from .i_database import IDatabase


class Database(IDatabase):
    @inject
    def __init__(self, settings: Settings):
        connect_args = {"check_same_thread": False}
        self.__engine = create_engine(
            settings.database_url,
            connect_args=connect_args
        )

    def create_database(self) -> None:
        SQLModel.metadata.create_all(self.__engine)

    def get_session(self) -> Session:
        return Session(self.__engine)
