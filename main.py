from src.logging.logger import logging
from src.exception.exception import CustomException
import os,sys
from src.entity.artifact_config import DataIngestionArtifact
from src.entity.entity_config import DataIngestionConfig,TrainingPipelineConfig
from src.components.ingestion import DataIngestion

if __name__ == "__main__":
    try:
        training_config = TrainingPipelineConfig()

        data_ingestion_config = DataIngestionConfig(training_config)
        data_ingestion_initiate = DataIngestion(data_ingestion_config)
        data_ingestion_artiact = data_ingestion_initiate.initiate_data_ingestion()

        print(data_ingestion_artiact)
        
    except Exception as e:
        raise CustomException(e,sys)