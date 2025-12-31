from src.logging.logger import logging
from src.exception.exception import CustomException
from src.utils.utils import (save_pickle_file, load_pickle_file, 
                             df_transform, save_numpy_obj)
from src.entity.entity_config import DataTransformationConfig
import os,sys
from src.constants import training_pipeline
from src.entity.artifact_config import DataTransformationArtifact,DataValidationArtifact

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

mapping = training_pipeline.DATA_TRANSFORMATION_FEATURE_MAPPING


class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config

            logging.info("DataTransformation initialized successfully.")
        except Exception as e:
            raise CustomException(e,sys)
    
    def get_transformations_pipeline(self):
        try:

                logging.info("Creating data transformation pipeline.")

                num_cols = ['weekly_hours', 'song_skip_rate', 'extrovertness_index']
                
                num_pipeline = Pipeline(steps=[
                                            ('imputer', KNNImputer(
                                                **training_pipeline.DATA_TRANSFORMATION_KNN_IMPUTE_PARAMS
                                            )),
                                            ('scaler', StandardScaler())])
                
                cat_cols = ['subscription_type','num_subscription_pauses','customer_service_inquiries',
                            'age_group','notif_segment']

                cat_pipeline = Pipeline(steps=[
                    ('imputer', SimpleImputer(
                        **training_pipeline.DATA_TRANSFORMATION_SMPLE_IMPUTE_PARAMS
                    ))
                ])

                preprocessor = ColumnTransformer(
                    transformers=[
                        ('num', num_pipeline, num_cols),
                        ('cat', cat_pipeline, cat_cols)
                    ]
                )

                logging.info(
                f"Transformation pipeline created | "
                f"Numerical cols: {len(num_cols)}, "
                f"Categorical cols: {len(cat_cols)}"
            )
                return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self):
         try:
              
              logging.info("Data transformation pipeline started.")

              status = self.data_validation_artifact.drift_status
              if status == False:
                   logging.warning(
                    "Data drift detected. Aborting data transformation stage."
                )
                   return f'Data Drift is too much to proceed'
              
              train_file_path = self.data_validation_artifact.valid_train_file_path
              test_file_path = self.data_validation_artifact.valid_test_file_path

              train_file, test_file = load_pickle_file(train_file_path), load_pickle_file(test_file_path)
              
              logging.info(
                f"Validated train/test data loaded | "
                f"Train shape: {train_file.shape}, "
                f"Test shape: {test_file.shape}"
            )
              logging.info(f'The columns for the app.py are{train_file.columns}')
              train_file_feature_engineered = df_transform(x=train_file, mapping=training_pipeline.DATA_TRANSFORMATION_FEATURE_MAPPING)
              test_file_feature_engineered = df_transform(x=test_file, mapping = training_pipeline.DATA_TRANSFORMATION_FEATURE_MAPPING)
              
            #   train_file_feature_engineered = train_file_feature_engineered.head(50)
            #   test_file_feature_engineered = test_file_feature_engineered.head(10)

              logging.info("Feature engineering completed on train and test data.")

              Target_col = training_pipeline.TARGET_COLUMN

              input_feature_train_df = train_file_feature_engineered.drop(columns=[Target_col])
              input_target_train_df = train_file_feature_engineered[[Target_col]]

              input_feature_test_df = test_file_feature_engineered.drop(columns=[Target_col])
              input_target_test_df = test_file_feature_engineered[[Target_col]]


              logging.info(f'{train_file_feature_engineered.head()}')
              preprocessor = self.get_transformations_pipeline()
              
              train_file_transformed = preprocessor.fit_transform(input_feature_train_df)
              test_file_transformed = preprocessor.transform(input_feature_test_df)

              logging.info(
                f"Data transformation completed | "
                f"Train transformed shape: {train_file_transformed.shape}, "
                f"Test transformed shape: {test_file_transformed.shape}"
            )

              train_arr = np.c_[train_file_transformed, input_target_train_df.to_numpy()]
              test_arr = np.c_[test_file_transformed, input_target_test_df.to_numpy()]
              
              save_numpy_obj(object_to_save=train_arr, file_path=self.data_transformation_config.transformed_train_file_path)
              save_numpy_obj(object_to_save=test_arr, file_path=self.data_transformation_config.transformed_test_file_path)
              save_pickle_file(file_to_save=preprocessor, file_path=self.data_transformation_config.trained_obj_file_path)

              save_pickle_file(file_path=r'final_obj/preprocessor.pkl',file_to_save=preprocessor)


              logging.info(
                "Transformation artifacts saved | "
                f"Train array: {self.data_transformation_config.transformed_train_file_path}, "
                f"Test array: {self.data_transformation_config.transformed_test_file_path}, "
                f"Preprocessor: {self.data_transformation_config.trained_obj_file_path}"
            )

              data_transformation_artifact = DataTransformationArtifact(
                   train_file_path=self.data_transformation_config.transformed_train_file_path,
                   test_file_path=self.data_transformation_config.transformed_test_file_path,
                    preprocessor_obj_path=self.data_transformation_config.trained_obj_file_path
              )

              logging.info("Data transformation pipeline completed successfully.")

              return data_transformation_artifact
         
         except Exception as e:
              raise CustomException(e,sys)