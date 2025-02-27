from us_visa.configuration.mongo_db_connection import MongoDbClient
from us_visa.constants import *
from us_visa.logger import logging
from us_visa.exception import USVisaException
import pandas as pd
import numpy as np
from typing import Optional
import sys

class USVisaData:
    def __init__(self):
        try:
            self.mongo_client = MongoDbClient(database_name=DATABASE_NAME)
        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)
    
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        try:   
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
                logging.info(f"Exporting data from collection: {collection_name} in database: {self.mongo_client.database_name}")
            else:
                collection = self.mongo_client[database_name][collection_name]
                logging.info(f"Exporting data from collection: {collection_name} in database: {database_name}")


            logging.info("Converting collection to DataFrame")
            df = pd.DataFrame(list(collection.find()))

            df.drop(columns=["_id"], errors="ignore", inplace=True)
            logging.info("Dropped '_id' column if it existed.")

            df.replace({"na": np.nan}, inplace=True)
            logging.info("Replaced 'na' with np.nan.")

            return df
        
        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)