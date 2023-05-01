from fastapi_injector import request_scope
from injector import singleton
from passlib.context import CryptContext

from src.authentication.authentication import Authentication
from src.authentication.i_authentication import IAuthentication
from src.authentication.i_password_handler import IPasswordHandler
from src.authentication.password_handler import PasswordHandler
from src.common.i_jwt_encoder import IJwtEncoder
from src.common.jwt_encoder import JwtEncoder
from src.common.settings import Settings
from src.database.database import Database
from src.database.i_database import IDatabase
from src.database.i_database_deleter import IDatabaseDeleter
from src.managers.i_user_manager import IUserManager
from src.managers.user_manager import UserManager
from src.multi_injector import MultiInjector

injector_instance = MultiInjector()

injector_instance.binder.bind(Settings, to=Settings, scope=singleton)
injector_instance.binder.bind(IJwtEncoder, JwtEncoder, scope=singleton)
injector_instance.binder.bind(
    CryptContext,
    to=CryptContext(schemes=["bcrypt"], deprecated=["auto"]),
    scope=singleton,
)
injector_instance.binder.bind_several(
    [IDatabase, IDatabaseDeleter], Database, scope=singleton
)
injector_instance.binder.bind(IPasswordHandler, to=PasswordHandler, scope=singleton)
injector_instance.binder.bind(IAuthentication, to=Authentication, scope=singleton)
injector_instance.binder.bind(IUserManager, to=UserManager, scope=request_scope)
