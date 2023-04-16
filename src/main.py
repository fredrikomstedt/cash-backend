from fastapi import FastAPI
from fastapi_injector import InjectorMiddleware, attach_injector
from injector import Injector

from src.authentication.api import router as auth_router
from src.dependencies import injector_instance


def create_app(injector: Injector):
    created_app = FastAPI(title='User Service')
    created_app.add_middleware(InjectorMiddleware, injector=injector)
    attach_injector(created_app, injector)
    created_app.include_router(auth_router)
    return created_app


app = create_app(injector_instance)
