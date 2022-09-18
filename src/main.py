from fastapi import FastAPI

from dependencies import create_database

app = FastAPI(title='Cash')


@app.on_event("startup")
def on_startup():
    create_database()
