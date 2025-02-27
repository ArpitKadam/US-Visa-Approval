import os
from us_visa.constants import *
from us_visa.logger import logging
from us_visa.exception import USVisaException
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DATA_INGESTION_CONFIG:
    trained_file_path: str
    test_file_path: str