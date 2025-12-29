from src.logging.logger import logging
from src.exception.exception import CustomException
from datetime import datetime
import os,sys
from src.constants import training_pipeline

class TrainingPipelineConfig:
    def __init__(self, timestamp = datetime.now()):
        try:
            timestamp = timestamp.strftime("%m-%d-%y-%H-%M-%S")
            self.artifact_name = training_pipeline.ARTIFACT_DIR
            self.artifact_dir = os.path.join(self.artifact_name, timestamp)
            self.model_dir = os.path.join('final_obj')
        except Exception as e:
            raise CustomException(e,sys)
        
class DataIngestionConfig:
    def __init__(self, training_config:TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(training_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR)

        self.feature_store_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_FILE_PATH,
                                                    training_pipeline.FILE_NAME)
        self.data_ingested_train_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DATA_PATH, 
                                                    training_pipeline.TRAIN_FILE_NAME)
        self.data_ingested_test_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DATA_PATH, 
                                                    training_pipeline.TEST_FILE_NAME)
        
        self.database_name = training_pipeline.DATABASE_NAME
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.table_name = training_pipeline.TABLE_NAME
        
class DataValidationConfig:
    def __init__(self, training_config:TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.data_validation_drift_report = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                                                         training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        
        self.valid_train_file_path = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR,
                                                  training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR,
                                                 training_pipeline.TEST_FILE_NAME)  
        self.invalid_train_file_path = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR,
                                                    training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR,
                                                   training_pipeline.TEST_FILE_NAME)