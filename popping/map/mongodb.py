from pymongo import MongoClient
from config.settings import env

# from pathlib import Path
# import environ

# env = environ.Env()

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# env_path = BASE_DIR / ".env"

# if env_path.exists():
#     with env_path.open("rt", encoding="utf8") as f:
#         env.read_env(f)

class MongoDBClient:
    _client = None
    _db = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = MongoClient(env('MONGO_URL'))
        return cls._client

    @classmethod
    def get_database(cls, db_name):
        if cls._db is None:
            cls._db = cls.get_client()[db_name]
        return cls._db

    @classmethod
    def get_collection(cls, db_name, collection_name):
        return cls.get_database(db_name)[collection_name]