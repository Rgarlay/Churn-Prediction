from src.logging.logger import logging
from src.exception.exception import CustomException
from src.utils.utils import (save_pickle_file, load_pickle_file, 
                             df_transform, save_numpy_obj, load_np_obj)
from src.entity.entity_config import ModelTrainerConfig
from src.entity.artifact_config import DataTransformationArtifact, ModelTrainerArtifact
import os,sys
from src.constants import training_pipeline
from src.utils.ml_utils.eval_models import evaluate_models, get_classification_score,ChurnModel

import pandas as pd
import numpy as np
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from xgboost import XGBClassifier
import mlflow.sklearn
import mlflow
import dagshub

dagshub.init(repo_owner='Rgarlay', repo_name='Churn-Prediction', mlflow=True)


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    
    def track_mlflow(self, bestmodel,classification_metric):
        try:
            mlflow.set_tracking_uri('https://dagshub.com/Rgarlay/Churn-Prediction.mlflow')
            with mlflow.start_run():
                mlflow.log_metric("accuracy", classification_metric.accuracy_score)
                mlflow.log_metric("f1_score", classification_metric.f1_score)
                mlflow.log_metric("recall", classification_metric.recall_score)
                mlflow.sklearn.log_model(sk_model=bestmodel,registered_model_name= "model")
        except Exception as e:
            raise CustomException(e,sys)
    

    def training_model(self, x_train,x_test,y_train,y_test):
        try:
            models = {
                'AdaBoost Classifier': AdaBoostClassifier(random_state=42),
                'RandomForest Classifier': RandomForestClassifier(random_state=42),
                'XGB Classifier': XGBClassifier(random_state=42,eval_metric='logloss')
            }

            params = {
                   'AdaBoost Classifier' : {
                        'n_estimators': [50, 100],
                        'learning_rate': [0.5, 1.0]
                    },
                    'RandomForest Classifier' : {
                        'n_estimators': [100, 200],
                        'max_depth': [None, 10, 20],
                        'min_samples_leaf': [1, 2],
                        'max_features': ['sqrt', 'log2']
                    },
                    'XGB Classifier': {
                        'n_estimators': [100, 200],
                        'max_depth': [3, 6],
                        'learning_rate': [0.1, 0.3],
                        'subsample': [0.8, 1.0],
                        'colsample_bytree': [0.8, 1.0]
                    }}
            
            report = evaluate_models(models = models, params = params,
                                 x_train = x_train,x_test = x_test,
                                 y_train=y_train,y_test = y_test)
            
            best_model_score = max(sorted(report.values()))
            best_model_name = list(report.keys())[list(report.values()).index(best_model_score)]

            best_model = models[best_model_name]

            y_train_pred = best_model.predict(x_train)

            y_test_pred = best_model.predict(x_test)

            #Train preds
            classification_train_metrics = get_classification_score(y_test=y_train, y_pred=y_train_pred)

            self.track_mlflow(bestmodel=best_model,classification_metric=classification_train_metrics)
            
            #Test preds
            classification_test_metrics = get_classification_score(y_test=y_test, y_pred=y_test_pred)

            self.track_mlflow(bestmodel=best_model,classification_metric=classification_test_metrics)


            preprocessor = load_pickle_file(self.data_transformation_artifact.preprocessor_obj_path)
            
            churn_model = ChurnModel(model=best_model, processor=preprocessor)
            save_pickle_file(file_path=self.model_trainer_config.trained_model_file_path, file_to_save=best_model)

            save_pickle_file(file_path=r'final_obj/model.pkl',file_to_save=best_model)

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                          train_metric_artifact=classification_train_metrics, test_metric_artifact=classification_test_metrics)
            

            return model_trainer_artifact
        

        
        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_model_training(self):
        try:
            train_file  = load_np_obj(self.data_transformation_artifact.train_file_path)
            test_file = load_np_obj(self.data_transformation_artifact.test_file_path)

            x_train,y_train,x_test,y_test = (
                train_file[:,:-1],
                train_file[:,-1],
                test_file[:,:-1],
                test_file[:,-1]
            )

            model_training_artifact = self.training_model(x_test=x_test,x_train=x_train,y_train=y_train,y_test=y_test)

            return model_training_artifact
        except Exception as e:
            raise CustomException(e,sys)