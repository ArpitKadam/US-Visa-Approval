import os
from dotenv import load_dotenv
import pymongo
import certifi
from us_visa.logger import logging
from us_visa.exception import USVisaException
import sys
import sys
load_dotenv()

ca = certifi.where()

DATABASE_NAME   = os.getenv("MONGO_DB_NAME")
MONGODB_URL_KEY = os.getenv("MONGO_DB_URI")

class MongoDbClient:
    client = None
    try:
        def __init__(self, database_name=DATABASE_NAME) -> None:
            if MongoDbClient.client is None:
                mongo_db_url = MONGODB_URL_KEY
                if mongo_db_url is None:
                    raise USVisaException("Environment Key Error: MONGO_DB_URI is not set", sys)
                
                MongoDbClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=certifi.where())
                self.client = MongoDbClient.client
                self.database = self.client[database_name]
                self.database_name = database_name
                logging.info(f"Connected successfully to {self.database_name} database")
                
    except Exception as e:
        raise USVisaException(e, sys)