import motor.motor_asyncio
from bson import ObjectId


class MongoRepository:
    def __init__(self, client):
        self.client: motor.motor_asyncio.AsyncIOMotorClient = client
        print(type(self.client))
        self.database = self.client["ChatAIDatabase"]

    async def init_new_chat(self, user_name: str, data: dict):
        collection = self.database[user_name]
        document = data
        result = await collection.insert_one(document)
        return str(result.inserted_id)

    async def get_chat_history(self, user_name: str, chat_id: str):
        collection = self.database[user_name]
        request = {'_id': ObjectId(chat_id)}
        result = await collection.find_one(request)
        result["_id"] = str(result["_id"])
        print(result)
        return result

    async def create_chat_history(self, user_name: str, chat_id: str, data: dict):
        collection = self.database[user_name]
        chat_id = ObjectId(chat_id)

        request = {'_id': chat_id}
        data = {'_id': chat_id, **data}
        result = await collection.replace_one(request, data)
        return result

    async def update_chat_history(self, user_name: str, chat_id: str, data: list[dict]):
        collection = self.database[user_name]
        request = {'_id': ObjectId(chat_id)}
        update_operation = {'$set': {
            "history": data
        }}
        result = await collection.update_one(request, update_operation)
        return result
