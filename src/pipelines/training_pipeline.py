from src.constants.training_pipeline import AWS_BUCKET_NAME
import os,sys
from src.exception.exception import CustomException
from src.logging.logger import logging

from src.entity.entity_config import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig
    )
from src.entity.artifact_config import (ModelTrainerArtifact,
                                           DataIngestionArtifact,
                                           DataTransformationArtifact,
                                           DataValidationArtifact)

from src.components.ingestion import DataIngestion,DataIngestionArtifact
from src.components.validation import DataValidation,DataValidationArtifact
from src.components.transformation import DataTransformation, DataValidationArtifact
from src.components.training import ModelTrainer,ModelTrainerArtifact

from src.cloud.s3_syncer import s3Sync



class TrainingPipeline:
    def __init__ (self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()
            self.sync_to_s3 = s3Sync()
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_ingestion(self):
        try:
            self.data_ingestion_config  = DataIngestionConfig(train_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_validation(self,data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                            data_validation_config=self.data_validation_config)
            
            data_validation_artifact = data_validation.initiate_data_validation()

            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                     data_transformation_config=self.data_transformation_config)
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()

            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_model_training(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_training_artifact: str = ModelTrainerConfig(self.training_pipeline_config)

            model_training = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                          model_trainer_config=self.model_training_artifact)
            
            model_training_artifact = model_training.initiate_model_training()

            return model_training_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def sync_artifact_to_s3(self):
        try:
            aws_bucket_url = f"s3://{AWS_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.sync_to_s3.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,
                                                                    aws_s3_bucket_url=aws_bucket_url)
        except Exception as e:
            raise CustomException(e,sys)

    def sync_saved_model_to_s3(self):
        try:
            aws_bucket_url = f"s3://{AWS_BUCKET_NAME}/final_obj/{self.training_pipeline_config.timestamp}"
            self.sync_to_s3.sync_folder_to_s3(folder = self.training_pipeline_config.model_dir,
                                                                    aws_s3_bucket_url=aws_bucket_url)
        except Exception as e:
            raise CustomException(e,sys)


    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.initiate_data_ingestion()
            data_validation_artifact = self.initiate_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.initiate_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.initiate_model_training(data_transformation_artifact=data_transformation_artifact)
            self.sync_artifact_to_s3()
            self.sync_saved_model_to_s3()

            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)