import yaml
from NetworkSecurity.expection.expection import NetworkSecurityExpection
from NetworkSecurity.logging.logger import logging
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