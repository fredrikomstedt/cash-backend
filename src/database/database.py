from global_dependencies import get_settings
from sqlmodel import Session, SQLModel, create_engine

connect_args = {"check_same_thread": False}
engine = create_engine(
    get_settings().database_url,
    connect_args=connect_args
)


def get_engine():
    return engine


def create_database():
    SQLModel.metadata.create_all(engine)


def get_database_session():
    with Session(engine) as session:
        yield session
