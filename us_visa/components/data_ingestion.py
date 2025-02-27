import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.exception import USVisaException
from us_visa.logger import logging
from us_visa.data_access.usvisa_data import USVisaData


class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            logging.error(USVisaException(e,sys))
            raise USVisaException(e,sys)
    

    def export_data_to_feature_store(self) -> pd.DataFrame:
        try:
            logging.info("Exporting data from MongoDB")
            usvisa_data = USVisaData()
            dataframe = usvisa_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info("Data exported successfully")
            logging.info(f"Dataframe shape: {dataframe.shape}")

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Saving data to feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info("Dataframe saved to feature store successfully")
            return dataframe
        
        except Exception as e:
            logging.error(USVisaException(e,sys))
            raise USVisaException(e,sys)
    

    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> None:
        try:
            logging.info("Splitting data into train and test sets")
            train_df, test_df = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Data split successfully")
            logging.info(f"Train dataframe shape: {train_df.shape}")
            logging.info(f"Test dataframe shape: {test_df.shape}")

            train_dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            test_dir_path = os.path.dirname(self.data_ingestion_config.test_file_path)
            os.makedirs(train_dir_path, exist_ok=True)
            os.makedirs(test_dir_path, exist_ok=True)
            logging.info(f"Saving train data to file path: {self.data_ingestion_config.train_file_path}")
            train_df.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            logging.info(f"Saving test data to file path: {self.data_ingestion_config.test_file_path}")
            test_df.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            logging.info("Data saved to file successfully")
            return None

        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)
        

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Initiating data ingestion")
            dataframe = self.export_data_to_feature_store()
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.train_file_path,
                                                            test_file_path=self.data_ingestion_config.test_file_path)
            logging.info("Data ingestion completed successfully")
            return data_ingestion_artifact

        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)