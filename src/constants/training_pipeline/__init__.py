import numpy as np


DATABASE_NAME: str = 'churn_db'
TABLE_NAME: str = 'churn'
ARTIFACT_DIR = 'archieve'
FILE_PATH: str = 'feature-csv'
TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'
FILE_NAME: str = 'feature.csv'
SCHEMA_FILE_PATH: str = 'data_schema\schema.yaml'
PREPROCESSING_OBJECT_FILE_NAME: str = 'preprocessor.pkl'
TARGET_COLUMN: str = 'churned'
AWS_BUCKET_NAME:str = 'churn-aws-bucket'

COLUMNS_TO_DROP =  ['index','location','payment_method',
                            'customer_id','payment_plan',
                            'signup_date','average_session_length',
                          'num_favorite_artists','num_playlists_created',
                          'weekly_songs_played', 'weekly_unique_songs']


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

'''
Constants for the transformation will start with DATA_TRANSFORMATION_
'''
DATA_TRANSFORMATION_DIR_NAME: str = 'data_transformation'
DATA_TRANSFORMATION_TRAIN_FILE_NAME: str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_NAME: str = "test.npy"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJ_DIR: str = "transformed_object"

DATA_TRANSFORMATION_FEATURE_MAPPING = {
                                                'customer_service_inquiries':
                                                    {'Low': 0, 'Medium': 1, 'High': 2},
                                                'subscription_type':
                                                    {'Free': 0, 'Student': 1, 'Family': 2, 'Premium': 3},
                                                'notif_segment':
                                                    {'Non-Engager': 0, 'Standard': 1, 'Extreme': 2},
                                                'age_group':
                                                    {'18-24': 2,'65-79': 2,'25-34': 1,
                                                    '55-64': 1,'35-44': 0,'45-54': 0 }
                                            }

DATA_TRANSFORMATION_KNN_IMPUTE_PARAMS: dict = {
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform"
}
DATA_TRANSFORMATION_SMPLE_IMPUTE_PARAMS: dict = {"strategy":'most_frequent'}

'''
Model Training constansts will begin with MODEL_TRAINER_
'''

MODEL_TRAINER_DIR_NAME: str = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR_NAME: str = 'trained_model'
MODEL_TRAINER_MODEL_NAME: str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD: str = 0.05