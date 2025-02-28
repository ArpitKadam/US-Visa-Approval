import boto3
import os
from us_visa.constants import *
from us_visa.logger import logging

class S3Client:
    s3_client = None
    s3_resource = None

    def __init__(self, region_name=AWS_REGION):
        if S3Client.s3_resource == None or S3Client.s3_client == None:
            __access_key_id = AWS_ACCESS_KEY_ID
            __secret_access_key = AWS_SECRET_ACCESS_KEY_ID
            if __access_key_id is None:
                logging.info("AWS_ACCESS_KEY_ID environment variable not found")
            if __secret_access_key is None:
                logging.info("AWS_SECRET_ACCESS_KEY_ID environment variable not found")

            S3Client.s3_resource = boto3.resource("s3",
                                                  aws_access_key_id = __access_key_id,
                                                  aws_secret_access_key = __secret_access_key,
                                                  region_name = region_name
                                                )
            S3Client.s3_client = boto3.client("s3",
                                              aws_access_key_id = __access_key_id,
                                              aws_secret_access_key = __secret_access_key,
                                              region_name = region_name
                                            )
            
            self.s3_client = S3Client.s3_client
            self.s3_resource = S3Client.s3_resource