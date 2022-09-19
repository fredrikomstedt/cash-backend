from fastapi_injector import request_scope
from injector import Injector, singleton
from passlib.context import CryptContext
from sqlmodel import Session, SQLModel, create_engine

from authentication.i_password_handler import IPasswordHandler
from authentication.password_handler import PasswordHandler
from database.database import Database
from database.i_database import IDatabase
from database.users.i_user_manager import IUserManager
from database.users.user_manager import UserManager
from settings import Settings

injector_instance = Injector()

injector_instance.binder.bind(Settings, to=Settings, scope=singleton)
injector_instance.binder.bind(CryptContext, to=CryptContext(
    schemes=['bcrypt'], deprecated=["auto"]), scope=singleton)
injector_instance.binder.bind(IDatabase, Database, scope=singleton)
injector_instance.binder.bind(
    IPasswordHandler, to=PasswordHandler, scope=singleton)
injector_instance.binder.bind(
    IUserManager, to=UserManager, scope=request_scope)
