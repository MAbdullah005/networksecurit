import yaml
from NetworkSecurity.expection.expection import NetworkSecurityExpection
from NetworkSecurity.logging.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score,precision_score,recall_score
import os,sys
import dill
import numpy as np
import pickle



def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as f:
            return yaml.safe_load(f)
    except Exception as e:
        NetworkSecurityExpection(e,sys)

def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as f:
            yaml.dump(content,f)
    except Exception as e:
        NetworkSecurityExpection(e,sys)

def save_numpy_array_data(file_path:str,array:np.array):
    """
    save numpy array data to 
    file path to location by creating 
    file
    """
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as f:
            np.save(f,array)
    except Exception as e:
        NetworkSecurityExpection(e,sys)

def save_object(file_path:str,obj:object)->None:
    try:
        logging.info("enter the save_object method of mainuils class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as f:
            pickle.dump(obj,f)
        logging.info("Exited the save_object method of mainutils class")
    except Exception as e:
        NetworkSecurityExpection(e,sys)


def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file Path {file_path} not exists")
        with open(file_path,'rb') as file:
            print(file)
            return pickle.load(file)
    except Exception as e:
        NetworkSecurityExpection(e,sys) 

def load_numpy_array_data(file_path:str)->np.array:
    """
    load the numpy array from file
    and read it and return for input
    to model
    """
    try:
        with open(file_path,'rb') as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityExpection(e,sys)
    

def evaluate_model(x_train,y_train,x_test,y_test,models,params):
    try:
        report={}
        for i in range(len(list(models))):
            model=list(models.values())[i]
            para=params[list(models.keys())[i]]
            gs=GridSearchCV(model,para,cv=3)
            gs.fit(x_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)

            y_train_pred=model.predict(x_train)

            y_test_pred=model.predict(x_test)

            trained_model_score=r2_score(y_train,y_train_pred)
            test_model_score=r2_score(y_test,y_test_pred)
            report[list(models.keys())[i]]=test_model_score

        return report

    except Exception as e:
        raise NetworkSecurityExpection(e,sys)