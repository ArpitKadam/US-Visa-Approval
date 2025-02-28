import boto3
import os
import sys
import pandas as pd
import pickle
from io import StringIO
from typing import Union, List
from botocore.exceptions import ClientError

from us_visa.configuration.aws_connection import S3Client
from us_visa.exception import USVisaException
from us_visa.logger import logging
from mypy_boto3_s3.service_resource import Bucket


class SimpleStorageService:
    def __init__(self):
        s3_client = S3Client()
        self.s3_client = s3_client.s3_client
        self.s3_resource = s3_client.s3_resource

    def get_bucket(self, bucket_name) -> Bucket:
        return self.s3_resource.Bucket(bucket_name)

    def s3_key_path_available(self, bucket_name, s3_key) -> bool:
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = list(bucket.objects.filter(Prefix=s3_key))
            return len(file_objects) > 0
        except Exception as e:
            logging.error(f"Error checking S3 key path: {e}")
            raise USVisaException(e, sys)

    @staticmethod
    def read_object(object_name: str, decode: bool = True, make_readable: bool = False) -> Union[StringIO, str]:
        try:
            raw_data = object_name.get()["Body"].read()
            decoded_data = raw_data.decode() if decode else raw_data
            return StringIO(decoded_data) if make_readable else decoded_data
        except Exception as e:
            logging.error(f"Error reading object: {e}")
            raise USVisaException(e, sys)

    def get_file_object(self, filename: str, bucket_name: str) -> Union[List[object], object]:
        try:
            bucket = self.get_bucket(bucket_name)
            list_of_files = list(bucket.objects.filter(Prefix=filename))
            return list_of_files[0] if len(list_of_files) == 1 else list_of_files
        except Exception as e:
            logging.error(f"Error getting file object: {e}")
            raise USVisaException(e, sys)

    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None) -> object:
        try:
            model_file = model_name if model_dir is None else os.path.join(model_dir, model_name)
            file_object = self.get_file_object(model_file, bucket_name)
            model_obj = self.read_object(file_object, decode=False)
            return pickle.loads(model_obj)
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            raise USVisaException(e, sys)

    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        try:
            self.s3_resource.Object(bucket_name, folder_name + "/").load()
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                self.s3_client.put_object(Bucket=bucket_name, Key=folder_name + "/")
            else:
                logging.error(f"Error creating folder: {e}")
                raise USVisaException(e, sys)

    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True):
        try:
            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)
            if remove:
                os.remove(from_filename)
        except Exception as e:
            logging.error(f"Error uploading file {from_filename} to {bucket_name}/{to_filename}: {e}")
            raise USVisaException(e, sys)

    def upload_df_as_csv(self, data_frame: pd.DataFrame, local_filename: str, bucket_filename: str, bucket_name: str) -> None:
        try:
            data_frame.to_csv(local_filename, index=False)
            self.upload_file(local_filename, bucket_filename, bucket_name)
        except Exception as e:
            logging.error(f"Error uploading DataFrame as CSV: {e}")
            raise USVisaException(e, sys)

    def read_csv(self, filename: str, bucket_name: str) -> pd.DataFrame:
        try:
            csv_obj = self.get_file_object(filename, bucket_name)
            return self.get_df_from_object(csv_obj)
        except Exception as e:
            logging.error(f"Error reading CSV from S3: {e}")
            raise USVisaException(e, sys)

    def get_df_from_object(self, object_: object) -> pd.DataFrame:
        try:
            content = self.read_object(object_, make_readable=True)
            return pd.read_csv(content, na_values="na")
        except Exception as e:
            logging.error(f"Error converting S3 object to DataFrame: {e}")
            raise USVisaException(e, sys)
