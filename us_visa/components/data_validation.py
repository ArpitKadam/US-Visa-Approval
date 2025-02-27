import json
import sys
import pandas as pd
import numpy as np
from us_visa.logger import logging
from us_visa.exception import USVisaException
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab, CatTargetDriftTab
from evidently.model_profile import Profile
from evidently.profile_sections import DataDriftProfileSection
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.constants import *
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)
        
    
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Length of columns in dataframe {len(dataframe.columns)}")
            logging.info(f"Length of columns in schema {len(self._schema_config['columns'])}")
            logging.info(f"Is all columns present in dataframe: {status}")
            return status
        except Exception as e:
            logging.error(USVisaException(e,sys))
            raise USVisaException(e, sys)
        
    
    def is_columns_exist(self, df: pd.DataFrame) -> bool:
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []

            for columns in self._schema_config["numerical_columns"]:
                if columns not in dataframe_columns:
                    missing_numerical_columns.append(columns)
            
            if len(missing_numerical_columns) > 0:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")
            
            for columns in self._schema_config["categorical_columns"]:
                if columns not in dataframe_columns:
                    missing_categorical_columns.append(columns)
            
            if len(missing_categorical_columns) > 0:
                logging.info(f"Missing categorical columns: {missing_categorical_columns}")

            return False if len(missing_numerical_columns) > 0 or len(missing_categorical_columns) > 0 else True
        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)
    

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)
    

    def detect_dataset_drift(self, reference_df: pd.DataFrame, current_df: pd.DataFrame) -> bool:
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(reference_df, current_df)
            report = data_drift_profile.json()
            json_report = json.loads(report)

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content= json_report)

            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            logging.info(f"{n_features} features detected")
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]
            logging.info(f"{n_drifted_features} drifted features detected")

            logging.info(f"{n_drifted_features}/{n_features} drift detected")
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]

            return drift_status
        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)
        
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            validation_error_msg = ""
            logging.info("Initiating data validation")
            train_df = DataValidation.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = DataValidation.read_data(self.data_ingestion_artifact.test_file_path)

            status = self.validate_number_of_columns(dataframe=train_df)
            logging.info(f"All columns present in training dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe"
                logging.info(validation_error_msg)

            status = self.validate_number_of_columns(dataframe=test_df)
            logging.info(f"All columns present in testing dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in testing dataframe"
                logging.info(validation_error_msg)
            
            status = self.is_columns_exist(df=train_df)
            logging.info(f"All required columns present in training dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe"
                logging.info(validation_error_msg)

            status = self.is_columns_exist(df=test_df)
            logging.info(f"All required columns present in testing dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in testing dataframe"
                logging.info(validation_error_msg)

            validation_status = len(validation_error_msg) == 0
            logging.info(f"Half Validation process is done and validation_status is {validation_status}")

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info(f"There is a drift in dataset")
                    validation_error_msg = "Drift Detected"
                else:
                    logging.info(f"There is no drift in dataset")
                    validation_error_msg = "No Drift Detected"
            else:
                logging.info(f"Validation process is not done")

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                data_validation_dir=self.data_validation_config.data_validation_dir,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact


        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)