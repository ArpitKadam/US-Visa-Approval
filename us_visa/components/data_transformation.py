import sys
import os
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer
from us_visa.constants import *
from us_visa.logger import logging
from us_visa.exception import USVisaException
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
)
from us_visa.utils.main_utils import save_numpy_array_data, save_object, read_yaml_file, drop_columns
from us_visa.entity.estimator import TargetValueMapping


class DataTransformation:
    def __init__(self,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        try:
            logging.info("Data Transformation Started")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            logging.error(USVisaException(e,sys))
            raise USVisaException(e, sys)
    

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)
        
    
    def get_data_transformation_object(self) -> Pipeline:
        try:
            logging.info("Data Transformation Object Started")

            numerical_transformer = StandardScaler()
            oh_transformer = OneHotEncoder()
            ordinal_encoder = OrdinalEncoder()
            logging.info("StandardScalar, OneHotEncoder, OrdinalEncoder loaded")

            oh_columns = self._schema_config["oh_columns"]
            or_columns = self._schema_config["or_columns"]
            transform_columns = self._schema_config["transform_columns"]
            num_features = self._schema_config["num_features"]

            logging.info(f"Columns loaded from schema file \n OH_COLUMNS: {oh_columns} \n OR_COLUMNS: {or_columns} \n TRANSFORM_COLUMNS: {transform_columns} \n NUM_FEATURES: {num_features}")

            transfrom_pipe = Pipeline(steps=[
                ('transformer', PowerTransformer(method='yeo-johnson'))
            ])
            logging.info("PowerTransformer loaded")

            preprocessor = ColumnTransformer([
                ("OneHotEncoder", oh_transformer, oh_columns),
                ("OrdinalEncode", ordinal_encoder, or_columns),
                ("Transformer", transfrom_pipe, transform_columns),
                ("StandardScaler", numerical_transformer, num_features)
            ])
            logging.info("ColumnTransformer loaded")
            logging.info("Prepocessor Object created successfully")

            return preprocessor

        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)
    

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            if self.data_validation_artifact.validation_status:
                preprocessor = self.get_data_transformation_object()

                train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
                test_df  = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)
                logging.info("Train and Test Data read successfully")

                input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_train_df = train_df[TARGET_COLUMN]
                logging.info("Train Input and Target Data separated")

                input_feature_train_df["company_age"] = CURRENT_YEAR - input_feature_train_df["yr_of_estab"]
                logging.info("Company Age feature created")

                drop_cols = self._schema_config["drop_columns"]
                input_feature_train_df = drop_columns(df=input_feature_train_df, columns=drop_cols)
                logging.info("Dropped columns from train data")
                logging.info(f"Train Data columns: {input_feature_train_df.columns}")
                logging.info(f"Train Data shape: {input_feature_train_df.shape}")

                target_feature_train_df = target_feature_train_df.replace(
                    TargetValueMapping()._asdict()
                )
                logging.info("Target Feature mapped for Train Data")


                input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_test_df = test_df[TARGET_COLUMN]
                logging.info("Test Input and Target Data separated")

                input_feature_test_df["company_age"] = CURRENT_YEAR - input_feature_test_df["yr_of_estab"]
                logging.info("Company Age feature created")

                input_feature_test_df = drop_columns(df=input_feature_test_df, columns=drop_cols)
                logging.info("Dropped columns from test data")
                logging.info(f"Test Data columns: {input_feature_test_df.columns}")
                logging.info(f"Test Data shape: {input_feature_test_df.shape}")

                target_feature_test_df = target_feature_test_df.replace(
                    TargetValueMapping()._asdict()
                )
                logging.info("Target Feature mapped for Test Data")

                logging.info("Applying preprocessor object on training data")
                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
                logging.info("Train data transformed successfully")

                logging.info("Applying preprocessor object on testing data")
                input_feature_test_arr = preprocessor.transform(input_feature_test_df)
                logging.info("Test data transformed successfully")

                logging.info("Applying SMOTEENN on Training Data")
                input_feature_train_final, target_feature_train_final = SMOTEENN(sampling_strategy="minority").fit_resample(
                    input_feature_train_arr, target_feature_train_df
                )
                logging.info("SMOTEENN applied on training data")

                logging.info("Applying SMOTEEN on Testing Data")
                input_feature_test_final, target_feature_test_final = SMOTEENN(sampling_strategy="minority").fit_resample(
                    input_feature_test_arr, target_feature_test_df
                )
                logging.info("SMOTEENN applied on testing data")

                logging.info("Creating train and test arrays")
                train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
                test_arr  = np.c_[input_feature_test_final, np.array(target_feature_test_final)]
                logging.info("Train and test arrays created")

                logging.info("Saving train and test arrays")
                save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, array=test_arr)
                logging.info("Train and test arrays saved")

                logging.info("Saving preprocessor object")
                save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocessor)
                logging.info("Preprocessor object saved")

                logging.info("Data Transformation Completed")

                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )
                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)
            
        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys)