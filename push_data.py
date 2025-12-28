import pandas as pd 
from sqlalchemy import create_engine, MetaData
import pymysql
from src.logging.logger import logging
from src.exception.exception import CustomException
import os,sys
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()


class PushingDataToMySQL():
    def __init__(self, db_name:str):
        try:
            self.db_name = db_name
        except Exception as e:
            raise CustomException(e,sys)

    def creating_db(self, connection_url: str, create_new_db:bool):
        '''
        Docstring for creating_db
        : connection_url: url to connect to the mysql database.
        :param db_name: name of the database.
        :param create_new_db:  Does the data base already exist or not?
        :type create_new_db: True if create new one, False if already exists.
        '''
        try:
            if create_new_db:
                engine = create_engine(connection_url, isolation_level="AUTOCOMMIT")
                with engine.connect() as con: 
                    con.execute(text(f'create database {self.db_name}'))
            engine = create_engine(f"{connection_url}/{self.db_name}") 
            self.engine = engine           
            return engine
        except Exception as e:
            raise CustomException(e,sys)
        
    def csv_to_sql(self, new_dataframe:pd.DataFrame,table_to_append_to, if_exists):
        try:
            '''
            Docstring for sql_to_csv

            :param new_dataframe: dataframe containing new records
            :type new_dataframe: pd.DataFrame
            :param table_to_append_to: table in db in which we want to append our records.
            : if_exists: 'append','replace'.
            '''
            with self.engine.connect() as con:
                existing_table = pd.read_sql(f'select * from {table_to_append_to} limit 1', con=con)
                if list(existing_table.columns) == list(new_dataframe.columns):
                    new_records = new_dataframe[~new_dataframe['customer_id'].isin(existing_table['customer_id'])]
                    new_records.to_sql(f'{table_to_append_to}', con = con,if_exists=if_exists)
                    return f"Data Successfully appended"
        except Exception as e:
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    mysql_url = os.getenv('mysql_string')
    pushing_data = PushingDataToMySQL(db_name='churn_db')
    engine = pushing_data.creating_db(connection_url=mysql_url,create_new_db=False)
    file_path = r'archieve\churn_data.csv'
    new_df = pd.read_csv(file_path)
    pushing_data.csv_to_sql(new_dataframe=new_df, table_to_append_to='churn', if_exists='replace')



   