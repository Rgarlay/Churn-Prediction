from src.logging.logger import logging
from src.exception.exception import CustomException
import os,sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import sqlalchemy
from dotenv import load_dotenv
from src.entity.entity_config import DataIngestionConfig
from src.constants.training_pipeline import DATABASE_NAME
from src.utils.utils import save_pickle_file,load_pickle_file
from src.entity.artifact_config import DataIngestionArtifact


load_dotenv()

url_path = f'{os.getenv('mysql_string')}/{DATABASE_NAME}'

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            logging.info("DataIngestion initialized with provided configuration.")
        except Exception as e:
            raise CustomException(e,sys)
        
    def importing_from_sql(self,connection_string_url:str) -> pd.DataFrame:
        '''
        Docstring for importing_from_sql
        
        :param connection_string_url: The connection string that has address to mysqlworkbench and database inside.
        :type connection_string_url: str
        :rtype: DataFrame
        '''
        try:
            logging.info("Starting data import from SQL database.")

            engine = sqlalchemy.create_engine(connection_string_url)
            with engine.connect() as con:
                dataframe = pd.read_sql(f"select * from {self.data_ingestion_config.table_name}", con=con)

                logging.info(
                f"Data successfully loaded from table "
                f"'{self.data_ingestion_config.table_name}' "
                f"with shape {dataframe.shape}."
            )
            
            cols_to_drop = ['index','location','payment_method',
                            'customer_id','payment_plan',
                            'signup_date','average_session_length',
                          'num_favorite_artists','num_playlists_created',
                          'weekly_songs_played', 'weekly_unique_songs']
        
            dataframe.drop(columns=[col for col in cols_to_drop if col in dataframe.columns],inplace=True)

            logging.info(
                f"Dropped {len(cols_to_drop)} columns. "
                f"Remaining columns: {list(dataframe.columns)}"
            )

            return dataframe
        except Exception as e:
            raise CustomException(e,sys)
    
    def saving_feature_file(self, dataframe:pd.DataFrame):
        '''
        Docstring for saving_feature_file
        
        :param self: The dataframe we are saving
        :param dataframe: pandas DataFrame
        :return: Pandas file will be saved as pickle file.
        '''
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_file_path),exist_ok=True)
            save_pickle_file(file_path=feature_store_file_path,file_to_save=dataframe)

            logging.info(
                f"Feature store file saved at '{feature_store_file_path}' "
                f"with shape {dataframe.shape}."
            )
        except Exception as e:
            raise CustomException(e,sys)
    
    def performing_train_test_split(self, dataframe:pd.DataFrame):
        try:
            
            train_file, test_file = train_test_split(dataframe, train_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
        
            train_file_path = self.data_ingestion_config.data_ingested_train_file_path
            test_file_path = self.data_ingestion_config.data_ingested_test_file_path

            dir_name = os.path.dirname(train_file_path)

            os.makedirs(dir_name, exist_ok= True)

            save_pickle_file(file_path=train_file_path, file_to_save=train_file)
            save_pickle_file(file_path=test_file_path, file_to_save=test_file)

            logging.info(
                f"Train-test split completed. "
                f"Train shape: {train_file.shape}, "
                f"Test shape: {test_file.shape}."
            )

            logging.info(
                f"Train data saved at '{train_file_path}', "
                f"Test data saved at '{test_file_path}'."
            )

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_ingestion(self):
        try:

            logging.info("Data ingestion pipeline started.")

            feature_file = self.importing_from_sql(connection_string_url=url_path)
            self.saving_feature_file(feature_file)
            self.performing_train_test_split(feature_file)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.data_ingested_train_file_path,
                                                            test_file_path=self.data_ingestion_config.data_ingested_test_file_path)

            logging.info("Data ingestion pipeline completed successfully.")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)