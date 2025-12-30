from src.logging.logger import logging
from src.exception.exception import CustomException
import os,sys
from src.entity.entity_config import (
    DataIngestionConfig,
    TrainingPipelineConfig,
    DataValidationConfig, DataTransformationConfig, ModelTrainerConfig)

from src.components.ingestion import DataIngestion
from src.components.validation import DataValidation
from src.components.transformation import DataTransformation
from src.components.training import ModelTrainer

if __name__ == "__main__":
    try:
        training_config = TrainingPipelineConfig()

        data_ingestion_config = DataIngestionConfig(training_config)
        data_ingestion_initiate = DataIngestion(data_ingestion_config)
        data_ingestion_artiact = data_ingestion_initiate.initiate_data_ingestion()

        data_validation_config = DataValidationConfig(training_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
                                         data_ingestion_artifact=data_ingestion_artiact)
        
        data_validation_config = data_validation.initiate_data_validation()

        data_transformation_config = DataTransformationConfig(training_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                                data_validation_artifact=data_validation_config)
        
        transformation_config = data_transformation.initiate_data_transformation()

        model_trainer_config = ModelTrainerConfig(training_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                     data_transformation_artifact=transformation_config)
        
        trainer_config = model_trainer.initiate_model_training()

        print(trainer_config)

        
    except Exception as e:
        raise CustomException(e,sys)