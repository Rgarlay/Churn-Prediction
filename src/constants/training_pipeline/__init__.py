

DATABASE_NAME: str = 'churn_db'
TABLE_NAME: str = 'churn'
ARTIFACT_DIR = 'archieve'
FILE_PATH: str = 'feature-csv'
TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'
FILE_NAME: str = 'feature.csv'
SCHEMA_FILE_PATH: str = 'data_schema\schema.yaml'


'''
constants for the ingestion will start with DATA_INGESTION_
'''

DATA_INGESTION_DIR: str = 'ingestion'
DATA_INGESTION_FEATURE_STORE_FILE_PATH: str = 'feature'
DATA_INGESTION_INGESTED_DATA_PATH: str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.25

'''
constantts for the validation will start with DATA_VALIDATION_
'''

DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_VALID_DIR: str = 'valid'
DATA_VALIDATION_INVALID_DIR: str = 'Invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = 'drift_report.yaml'

