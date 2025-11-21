# app/repositories/mongo_client.py
from pymongo import MongoClient
from app.config.settings import settings


class MongoClientFactory:
    _client: MongoClient | None = None

    @classmethod
    def get_client(cls) -> MongoClient:
        if cls._client is None:
            cls._client = MongoClient(settings.mongo_uri)
        return cls._client

    @classmethod
    def get_db(cls):
        client = cls.get_client()
        return client[settings.mongo_db_name]
