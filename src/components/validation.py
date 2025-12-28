from src.logging.logger import logging
from src.exception.exception import CustomException
import os,sys
import pandas as pd
from src.utils.utils import save_pickle_file,load_pickle_file
from src.entity.entity_config import DataValidationConfig
from src.entity.artifact_config import DataIngestionArtifact
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self, data_validation_config:DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
    
    