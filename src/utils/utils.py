from src.exception.exception import CustomException
import os,sys
import pickle
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np


def df_transform(x: pd.DataFrame, mapping:dict):
        try:
            x_copy = x.copy()

            # ----- age group -----
            bins = [18, 25, 35, 45, 55, 65, 80]
            labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65-79']
            x_copy['age_group'] = pd.cut(
                x_copy['age'],
                bins=bins,
                labels=labels,
                right=False
            )

            # ----- notification segment -----
            x_copy['notif_segment'] = pd.cut(
                x_copy['notifications_clicked'],
                bins=[-1, 4, 44, float('inf')],
                labels=['Non-Engager', 'Standard', 'Extreme']
            )

            x_copy['extrovertness_index'] = (
                x_copy['num_shared_playlists'] /
                (x_copy['num_platform_friends'] + 1)
            )

            for col, func in mapping.items():
                    x_copy[col] = x_copy[col].map(func)

            x_copy.drop(
                columns=[
                    'age',
                    'notifications_clicked',
                    'num_shared_playlists',
                    'num_platform_friends'
                ],
                inplace=True
            )

            return x_copy

        except Exception as e:
            raise CustomException(e, sys)
        
        
def load_yaml_file(file_path):
    try:
        import yaml
        with open(file_path, 'rb') as file:
            lines = yaml.safe_load(file)
        return lines
    except Exception as e:
        raise CustomException(e,sys)

def save_yaml_file(file_path, content, replace):
    try:
        import yaml
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.safe_dump(content,file)
    except Exception as e:
        raise CustomException(e,sys)
    
def save_pickle_file(file_to_save, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            pickle.dump(file_to_save, file)
    except Exception as e:
        raise CustomException(e,sys)

def load_pickle_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            lines = pickle.load(file)
            return lines
    except Exception as e:
        raise CustomException(e,sys)
    
def save_numpy_obj(object_to_save,file_path):
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, object_to_save)
    except Exception as e:
        raise CustomException(e,sys)
    
def load_np_obj(file_path):
    try:
        with open(file_path, 'rb') as file:
            return np.load(file, allow_pickle=True)
    except Exception as e:
        raise CustomException(e,sys)









