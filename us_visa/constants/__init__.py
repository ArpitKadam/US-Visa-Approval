from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()

DATABASE_NAME   = os.getenv("MONGO_DB_NAME")
MONGODB_URL_KEY = os.getenv("MONGO_DB_URI")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
BUCKET_NAME = os.getenv("MODEL_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY_ID = os.getenv("AWS_SECRET_ACCESS_KEY_ID")
AWS_REGION = os.getenv("AWS_REGION")

PIPELINE_NAME: str = "us-visa-pipeline"
ARTIFACT_DIR: str  = "Artifacts"
MODEL_FILE_NAME: str = "final_model.pkl"

FILE_NAME: str = "usvisa.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

TARGET_COLUMN: str = "case_status"
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

"""
DATA TRANSFORMATION CONSTANTS
"""

"""
DATA INGESTION CONSTANTS
"""

DATA_INGESTION_COLLECTION_NAME: str = COLLECTION_NAME
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
DATA VALIDATION CONSTANTS
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

"""
DATA TRANSFORMATION CONSTANTS
"""

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed_data"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DATA_FILE_NAME: str = "train.npy"
DATA_TRANSFORMATION_TRANSFORMED_TEST_DATA_FILE_NAME: str = "test.npy"
DATA_TRANSFORMATION_PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"

"""
MODEL TRAINING CONSTANTS
"""

MODEL_TRAINER_DIR_NAME: str = "model_training"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "final_model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.7
MODEL_TRAINER_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")

"""
MODEL EVALUATION CONSTANTS
"""

MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_BUCKET_NAME: str = os.getenv("MODEL_BUCKET_NAME")
MODEL_PUSH_S3_KEY: str = os.getenv("MODEL_PUSHER_S3_KEY")
