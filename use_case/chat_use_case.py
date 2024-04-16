import motor.motor_asyncio

from repositories.NLP_AI import J2ChatAI
from repositories.mongo_rep import MongoRepository


class ChatUseCase:
    def __init__(self, mongo_rep, chat_service):
        self.mongo_rep: MongoRepository = mongo_rep
        self.chat_service: J2ChatAI = chat_service

    async def init_new_chat(self, model_description: str, user_name: str):
        data = {'model_description': model_description}
        res = await self.mongo_rep.init_new_chat(user_name, data)
        return {"chat_id": res}

    async def chat_request(self, text: str, user_name: str, chat_id: str):

        conversation = await self.mongo_rep.get_chat_history(user_name, chat_id)
        history: list = conversation.get('history', None)
        model_description = conversation.get('model_description')

        if history:
            messages = history[-5:]
            answer_from_chat = await self.chat_service.make_request_to_chat(messages,
                                                                            model_description=model_description)
            answered_text = answer_from_chat['outputs'][0]['text']

            new_message_user = {"text": text, "role": "user"}
            new_message_assistant = {"text": answered_text, "role": "assistant"}
            updated_history = history[:]
            updated_history.append(new_message_user)
            updated_history.append(new_message_assistant)
            result = await self.mongo_rep.update_chat_history(user_name, chat_id, updated_history)

            print(result)

        else:
            new_history = [{"text": text, "role": "user"}]
            answer_from_chat = await self.chat_service.make_request_to_chat(new_history,
                                                                            model_description=model_description)
            answered_text = answer_from_chat['outputs'][0]['text']

            print(answered_text)
            new_history.append({"text": answered_text, "role": "assistant"})

            data_for_storing = {'model_description': model_description, 'history': new_history}
            status = await self.mongo_rep.create_chat_history(user_name, chat_id, data_for_storing)
            print(status)
        return answered_text

    async def get_chat_history(self, user_name: str, chat_id: str):
        conversation = await self.mongo_rep.get_chat_history(user_name, chat_id)
        response = conversation.get('history', None)
        return response
