import sys
from typing import Tuple
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, confusion_matrix, classification_report
from neuro_mf import ModelFactory
from us_visa.exception import USVisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import load_numpy_array_data, read_yaml_file, load_object, save_object
from us_visa.entity.config_entity import ModelTrainerConfig
from us_visa.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from us_visa.entity.estimator import USvisaModel


class ModelTrainer:
    def __init__(self,
                data_transformation_artifact: DataTransformationArtifact,
                model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self, train: np.array, test:np.array) -> Tuple[object, object]:
        try:
            logging.info("Using neuro_mf to get best model object and report")
            model_fractory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)

            x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]
            logging.info("Extracted x_train, y_train, x_test, y_test from train and test array")
            logging.info(f"x_train: {len(x_train)}, y_train: {len(y_train)}, x_test: {len(x_test)}, y_test: {len(y_test)}")

            logging.info("Fitting the model into neuro_mf")
            best_model_detail = model_fractory.get_best_model(X=x_train, y=y_train, base_accuracy=self.model_trainer_config.expected_accuracy)
            model_obj = best_model_detail.best_model
            logging.info("Best model has been found on us visa data")

            y_pred = model_obj.predict(x_test)
            logging.info("Predicted the values using best model")

            acc = accuracy_score(y_test, y_pred)
            f1  = f1_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)
            rec = recall_score(y_test, y_pred)
            roc_sc = roc_auc_score(y_test, y_pred)
            cnf = confusion_matrix(y_test, y_pred)
            clf_rep = classification_report(y_test, y_pred)
            logging.info("Calculated the metrics for the best model")
            logging.info(f"Accuracy: {str(acc)} \n F1_Score: {str(f1)} \n Precision: {str(prec)} \n Recall: {str(rec)} \n ROC_AUC_Score: {str(roc_sc)} \n Confusion_Matrix: {str(cnf)} \n Classification_Report: {str(clf_rep)}")

            metric_artifact = ClassificationMetricArtifact(f1_score=f1, precision_score=prec, recall_score=rec, accuracy_score=acc, roc_auc_score=roc_sc, confusion_matrix=cnf, classification_report=clf_rep)
            return best_model_detail, metric_artifact

        except Exception as e:
            logging.info(USVisaException(e, sys))
            raise USVisaException(e, sys)
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("Initiating model trainer")
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
            logging.info("Loaded train and test array")

            best_model_detail, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)
            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
            if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                raise Exception("No best model found with an accuracy greater than the base accuracy")
            
            usvisa_model = USvisaModel(preprocessing_object=preprocessing_obj, trained_model_object=best_model_detail.best_model)
            logging.info("Created usvisa model on train and test dataset")
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=usvisa_model)
            logging.info(f"Best model save at filepath {self.model_trainer_config.trained_model_file_path}")

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path, metric_artifact=metric_artifact)

            return model_trainer_artifact
        except Exception as e:
            logging.info(USVisaException(e, sys))
            raise USVisaException(e, sys)