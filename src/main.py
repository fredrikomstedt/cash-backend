from fastapi import FastAPI
from fastapi_injector import InjectorMiddleware, attach_injector

from src.authentication.api import router as auth_router
from src.database.i_database import IDatabase
from src.dependencies import injector_instance

app = FastAPI(title='User Service')
app.add_middleware(InjectorMiddleware, injector=injector_instance)
attach_injector(app, injector_instance)


app.include_router(auth_router)
