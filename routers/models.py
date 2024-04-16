from pydantic import BaseModel


class InitModel(BaseModel):
    chat_description: str


class MessageModel(BaseModel):
    message: str
