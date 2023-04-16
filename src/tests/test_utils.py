from unittest.mock import MagicMock

from injector import singleton

from src.common.settings import Settings
from src.database.database import Database
from src.database.i_database import IDatabase
from src.database.i_database_deleter import IDatabaseDeleter
from src.multi_injector import MultiInjector


def create_injector_with_database():
    injector = MultiInjector()
    injector.binder.bind(Settings, to=MagicMock(), scope=singleton)
    injector.get(Settings).database_url = "sqlite:///test_database.db"
    injector.binder.bind_several(
        [IDatabase, IDatabaseDeleter], Database, scope=singleton)

    return injector
