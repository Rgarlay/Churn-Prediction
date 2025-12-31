from src.logging.logger import logging
from src.exception.exception import CustomException
from datetime import datetime
import os,sys
from src.constants import training_pipeline

class TrainingPipelineConfig:
    def __init__(self, timestamp = datetime.now()):
        try:
            self.timestamp = timestamp.strftime("%m-%d-%y-%H-%M-%S")
            self.artifact_name = training_pipeline.ARTIFACT_DIR
            self.artifact_dir = os.path.join(self.artifact_name, self.timestamp)
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

class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir:str =  os.path.join(training_pipeline_config.artifact_dir, 
                                                         training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        
        self.transformed_train_file_path: str =  os.path.join(self.data_transformation_dir, 
                                                  training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, 
                                                  training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),)
        
        self.transformed_test_file_path: str =  os.path.join(self.data_transformation_dir,
                                                 training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, 
                                                  training_pipeline.TEST_FILE_NAME.replace('csv','npy'), )      ##can remove comma
        self.trained_obj_file_path = os.path.join(self.data_transformation_dir,                                 ##it just makes the 
                                                  training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJ_DIR,    ##bracket a tuple.
                                                  training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,)

class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        self.model_train_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path: str = os.path.join(self.model_train_dir,
                                                    training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR_NAME,
                                                    training_pipeline.MODEL_TRAINER_MODEL_NAME)
        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold: float = training_pipeline.MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD

        