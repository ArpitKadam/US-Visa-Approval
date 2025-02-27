import os
import sys
from us_visa.exception import USVisaException
from us_visa.logger import logging
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.entity.config_entity import (DataIngestionConfig,
                                          DataValidationConfig)
from us_visa.entity.artifact_entity import (DataIngestionArtifact,
                                            DataValidationArtifact)

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()

    
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
        

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info("Starting data validation")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data validation completed successfully")
            logging.info("="*30)
            return data_validation_artifact

        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)
        
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)