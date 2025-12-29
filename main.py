from src.logging.logger import logging
from src.exception.exception import CustomException
import os,sys
from src.entity.entity_config import (
    DataIngestionConfig,
    TrainingPipelineConfig,
    DataValidationConfig)
from src.components.ingestion import DataIngestion
from src.components.validation import DataValidation

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

        print(data_validation_config)
        
    except Exception as e:
        raise CustomException(e,sys)