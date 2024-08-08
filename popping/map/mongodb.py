from pymongo import MongoClient

class MongoDBClient:
    _client = None
    _db = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = MongoClient('mongodb://localhost:27017/')
        return cls._client

    @classmethod
    def get_database(cls, db_name):
        if cls._db is None:
            cls._db = cls.get_client()[db_name]
        return cls._db

    @classmethod
    def get_collection(cls, db_name, collection_name):
        return cls.get_database(db_name)[collection_name]