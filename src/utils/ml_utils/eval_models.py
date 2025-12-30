import numpy as np
from src.logging.logger import logging
from src.exception.exception import CustomException
import os,sys
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import recall_score
from src.entity.artifact_config import ClassificationMetricArtifact
from sklearn.metrics import accuracy_score, recall_score, f1_score


def evaluate_models(models: dict, params:dict, x_train,x_test,y_train,y_test):
    try:
        report = {}
        for i in range(len(models)):

            model = list(models.values())[i]
            param = list(params.values())[i]

            grid = GridSearchCV(model, param_grid=param, cv = 2)

            grid.fit(x_train,x_test)

            model.set_params(**grid.best_params_)
            model.fit(x_train,x_test)
            
            y_pred = model.predict(y_train)
            
            test_r2_score = recall_score(y_true=y_test, y_pred=y_pred)

            
            report[list(models.keys())[i]] = test_r2_score
        
        return report

    except Exception as e:
        raise CustomException(e,sys)
    

def get_classification_score(y_test, y_pred):
    try:
        accuracy = accuracy_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        classification_artifact = ClassificationMetricArtifact(
            accuracy_score=accuracy,
            recall_score=recall,
            f1_score=f1
        )

        logging.info(
            f"Classification Metrics — Accuracy: {accuracy}, Recall: {recall}, F1 Score: {f1}"
        )

        return classification_artifact

    except Exception as e:
        raise CustomException(e, sys)



class ChurnModel:
    def __init__(self,processor, model):
        try:
            self.model = model
            self.processor = processor
        except Exception as e:
            raise CustomException(e,sys)
    
    def predict(self,x):

        try:
            X_transform = self.processor.transform(x)
            y_hat = self.model.predict(X_transform)
            return y_hat
        except Exception as e:
            raise CustomException(e,sys)