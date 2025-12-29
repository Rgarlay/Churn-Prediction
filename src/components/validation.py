from src.logging.logger import logging
from src.exception.exception import CustomException
import os,sys
import pandas as pd
from src.utils.utils import save_pickle_file,load_pickle_file, load_yaml_file, save_yaml_file
from src.entity.entity_config import DataValidationConfig
from src.entity.artifact_config import DataIngestionArtifact
from scipy.stats import ks_2samp
from src.constants.training_pipeline import SCHEMA_FILE_PATH
from src.entity.artifact_config import DataValidationArtifact


class DataValidation:
    def __init__(self, data_validation_config:DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_file = load_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise CustomException(e,sys)
    
    def validation_of_no_cols(self, dataframe):
        '''
        new_dataframe: our new dataframe.
        '''
        try:
            standard_no_of_cols = len(self.schema_file['columns'])
            no_of_cols_in_df = len(list(dataframe.columns))
            if standard_no_of_cols == no_of_cols_in_df:
                return True
            return False
        
        except Exception as e:
            raise CustomException(e,sys)
        
    
    def detect_data_drift(self, new_df, old_df, threshold):
        try:
            status = True   ## Both distributions are the same.
            drift_dict = {}
            for i in self.schema_file['continuous_numerical_columns']:
                is_same_dict = ks_2samp(old_df[i],new_df[i])
                if threshold <= is_same_dict.pvalue:
                    is_drift_found = False
                else:
                    is_drift_found = True
                    status = False
                drift_dict.update({i: {
                                        'pvalue': float(is_same_dict.pvalue),
                                        'is_drift_found': bool(is_drift_found)
                                    }
                                })
                
                drift_report_file_path = self.data_validation_config.data_validation_drift_report

                os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)

                save_yaml_file(file_path=drift_report_file_path, content=drift_dict, replace=True)

            return status
        ##Idea is that if the status is False, then we do not trin the model. And transformation will understand that via
        ## data validation artifact.
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_validation(self):
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_file = load_pickle_file(train_file_path)
            test_file = load_pickle_file(test_file_path)

            no_of_cols_status:bool = self.validation_of_no_cols(test_file)

            drift_status: bool = self.detect_data_drift(new_df=test_file, old_df=train_file,threshold=0.05)

            if (drift_status == False) or (no_of_cols_status== False):

                train_file_save_path = self.data_validation_config.invalid_train_file_path
                test_file_save_path = self.data_validation_config.invalid_test_file_path
            else:
                train_file_save_path = self.data_validation_config.valid_train_file_path
                test_file_save_path = self.data_validation_config.valid_test_file_path

            save_pickle_file(file_to_save=train_file, file_path=train_file_save_path)                
            save_pickle_file(file_to_save=test_file, file_path=test_file_save_path)    



            data_validation_artifact = DataValidationArtifact(
                drift_status=drift_status,
                no_of_cols_status=no_of_cols_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.data_validation_drift_report
            )
            
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e,sys)
        