import os
import sys
from us_visa.exception import USVisaException
from us_visa.logger import logging
from us_visa.components.data_ingestion import DataIngestion
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed successfully")
            logging.info("="*30)
            return data_ingestion_artifact

        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)
        
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            return data_ingestion_artifact

        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)