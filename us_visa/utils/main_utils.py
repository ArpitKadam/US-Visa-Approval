import os
import sys
from us_visa.logger import logging
from us_visa.exception import USVisaException
import numpy as np
import dill
import yaml
import pandas as pd
from pathlib import Path


def read_yaml_file(file_path: str) -> dict:
    try:
        logging.info(f"Reading yaml file from {file_path}")
        with open(file_path, "rb") as files:
            data = yaml.safe_load(files)
            logging.info(f"Yaml file read successfully from {file_path}")
            return data
    except Exception as e:
        logging.error(f"Error reading yaml file from {file_path}")
        raise USVisaException(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        logging.info(f"Writing YAML file to {file_path}")
        directory = Path(file_path).parent
        directory.mkdir(parents=True, exist_ok=True)
        # Replace file if requested
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        # Write YAML file
        with open(file_path, "w") as file:
            yaml.dump(content, file)
            logging.info(f"YAML file written successfully to {file_path}")
    except Exception as e:
        logging.error(f"Error writing YAML file to {file_path}")
        raise USVisaException(e, sys) from e


def load_object(file_path: str) -> object:
    try:
        logging.info(f"Loading object from {file_path}")
        with open(file_path, "rb") as files:
            obj = dill.load(files)
            logging.info(f"Object loaded successfully from {file_path}")
            return obj
    except Exception as e:
        logging.error(f"Error loading object from {file_path}")
        raise USVisaException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.array) -> None:
    try:
        logging.info(f"Saving numpy array data to {file_path}")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as files:
            np.save(files, array)
            logging.info(f"Data saved successfully to {file_path}")
    except Exception as e:
        logging.error(f"Error saving numpy array data to {file_path}")
        raise USVisaException(e, sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    try:
        logging.info(f"Loading numpy array data from {file_path}")
        with open(file_path, "rb") as files:
            array = np.load(files)
            logging.info(f"Data loaded successfully from {file_path}")
            return array
    except Exception as e:
        logging.error(f"Error loading numpy array data from {file_path}")
        raise USVisaException(e, sys) from e

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info(f"Saving object to {file_path}")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as files:
            dill.dump(obj, files)
            logging.info(f"Object saved successfully to {file_path}")
    except Exception as e:
        logging.error(f"Error saving object to {file_path}")
        raise USVisaException(e, sys) from e


def drop_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    try:
        logging.info(f"Dropping columns from DataFrame: {columns}")
        df = df.drop(columns=columns)
        logging.info(f"Columns dropped successfully from DataFrame: {columns}")
        return df
    except Exception as e:
        logging.error(f"Error dropping columns from DataFrame: {columns}")
        raise USVisaException(e, sys) from e