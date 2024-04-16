from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession

from repositories.mongodb_client import get_async_mongo_client
from repositories.NLP_AI import J2ChatAI
from repositories.mongo_rep import MongoRepository
from use_case.chat_use_case import ChatUseCase


async def get_mongo() -> AsyncIOMotorClientSession:
    async with await get_async_mongo_client.client.start_session() as session:
        async with session.start_transaction():
            yield await get_async_mongo_client()


def get_mongo_repository(client=Depends(get_mongo)):
    return MongoRepository(client)


def get_chat_use_case(mongo_rep: MongoRepository = Depends(get_mongo_repository), chat_ai: J2ChatAI = Depends()):
    return ChatUseCase(mongo_rep, chat_ai)
