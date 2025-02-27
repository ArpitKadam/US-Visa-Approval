from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME   = os.getenv("MONGO_DB_NAME")
MONGODB_URL_KEY = os.getenv("MONGO_DB_URI")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

PIPELINE_NAME: str = "us-visa-pipeline"
ARTIFACT_DIR: str  = "Artifacts"
MODEL_FILE_NAME: str = "model.pkl"
SCALER_FILE_NAME: str = "scaler.pkl"

FILE_NAME: str = "usvisa.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

"""
DATA INGESTION CONSTANTS
"""

DATA_INGESTION_COLLECTION_NAME: str = COLLECTION_NAME
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
"""

