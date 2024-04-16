import motor.motor_asyncio


class AsyncMongoDBClient:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019/?replicaSet=rs0")

    async def __call__(self, *args, **kwargs) -> motor.motor_asyncio.AsyncIOMotorClient:
        return self.client


get_async_mongo_client = AsyncMongoDBClient()
