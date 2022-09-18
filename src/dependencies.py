from functools import lru_cache
from settings import Settings
from sqlmodel import SQLModel, create_engine, Session


@lru_cache()
def get_settings():
    return Settings()


connect_args = {"check_same_thread": False}
engine = create_engine(
    get_settings().database_url,
    connect_args=connect_args
)


def create_database() -> None:
    SQLModel.metadata.create_all(engine)


def get_database_session() -> Session:
    with Session(engine) as session:
        yield session
