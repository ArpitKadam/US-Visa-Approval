import sys, os
from us_visa.cloud_storage.aws_storage import SimpleStorageService
from us_visa.exception import USVisaException
from us_visa.logger import logging
from us_visa.entity.s3_estimator import USvisaEstimator
from us_visa.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from us_visa.entity.config_entity import ModelPusherConfig



class ModelPusher:
    def __init__(self, 
                 model_pusher_config: ModelPusherConfig, 
                 model_evaluation_artifact: ModelEvaluationArtifact):
        self.s3 = SimpleStorageService()
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.usvisa_estimator = USvisaEstimator(
            bucket_name=model_pusher_config.bucket_name,
            model_path=model_pusher_config.s3_model_key_path
        )
    

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            logging.info("Starting model pusher")
            self.usvisa_estimator.save_model(from_file=self.model_evaluation_artifact.trained_model_path)
            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.s3_model_key_path
            )
            logging.info("Uploaded artifacts folder successfully to S3 Bucket")
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            logging.info("Model pusher completed successfully")

            return model_pusher_artifact
        except Exception as e:
            logging.error(f"Error during model pusher initiation: {e}")
            raise USVisaException(e, sys)