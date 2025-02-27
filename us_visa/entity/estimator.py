import sys
import os
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from us_visa.logger import logging
from us_visa.exception import USVisaException


class TargetValueMapping:
    def __init__(self):
        self.Certified:int = 0
        self.Denied:int = 1
    
    def _asdict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))
    

class USvisaModel:
    def __init__(self,preprocessing_object:Pipeline, trained_model_object: object):
        try:
            self.preprocessing_object = preprocessing_object
            self.trained_model_object = trained_model_object
        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys) from e

    def predict(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            transformedfeatures = self.preprocessing_object.transform(dataframe)
            return self.trained_model_object.predict(transformedfeatures)
        
        except Exception as e:
            logging.error(USVisaException(e, sys))
            raise USVisaException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"
    
    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"