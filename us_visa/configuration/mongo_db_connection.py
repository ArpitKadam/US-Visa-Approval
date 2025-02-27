import os
from dotenv import load_dotenv
import pymongo
import certifi
from us_visa.logger import logging
from us_visa.exception import USVisaException
import sys

load_dotenv()

ca = certifi.where()

DATABASE_NAME   = os.getenv("MONGO_DB_NAME")
MONGODB_URL_KEY = os.getenv("MONGO_DB_URI")

class MongoDbClient:
    client = None

    def __init__(self, database_name = DATABASE_NAME) -> None:
        try:
            if MongoDbClient.client is None:
                mongo_db_url = MONGODB_URL_KEY
                if mongo_db_url is None:
                    raise Exception(f"Environment key for mongodb url is not set")
                MongoDbClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile = ca)
            self.client = MongoDbClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection established successfully")
        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)