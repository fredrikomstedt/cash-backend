from fastapi import FastAPI
from fastapi_injector import InjectorMiddleware, attach_injector

from database.i_database import IDatabase
from dependencies import injector_instance

app = FastAPI(title='Cash')
app.add_middleware(InjectorMiddleware, injector=injector_instance)
attach_injector(app, injector_instance)


@app.on_event("startup")
def on_startup():
    injector_instance.get(IDatabase).create_database()
