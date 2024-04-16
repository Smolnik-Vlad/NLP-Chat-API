from fastapi import FastAPI

from routers.chat_router import chat_router
from settings import settings

app = FastAPI()

app.include_router(chat_router, prefix='/chat_router')


@app.get("/")
async def root():
    print(settings.chat_api_key)
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
