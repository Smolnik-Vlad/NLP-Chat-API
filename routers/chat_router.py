from fastapi import APIRouter, Depends

from depends import get_chat_use_case

from routers.models import InitModel, MessageModel
from use_case.chat_use_case import ChatUseCase

chat_router = APIRouter()


@chat_router.post("/new_chat")
async def new_chat(user_name: str, chat_data: InitModel, chat_use_case: ChatUseCase = Depends(get_chat_use_case)):
    result = await chat_use_case.init_new_chat(model_description=chat_data.chat_description, user_name=user_name)
    return result


@chat_router.post("/chat_request")
async def create_request_to_chat(user_name: str, chat_id: str, message: MessageModel,
                                 chat_use_case: ChatUseCase = Depends(get_chat_use_case)):
    result = await chat_use_case.chat_request(message.message, user_name, chat_id)
    return result


@chat_router.get("/chat_history")
async def get_chat_history(user_name: str, chat_id: str, chat_use_case: ChatUseCase = Depends(get_chat_use_case)):
    result = await chat_use_case.get_chat_history(user_name, chat_id)
    return result
