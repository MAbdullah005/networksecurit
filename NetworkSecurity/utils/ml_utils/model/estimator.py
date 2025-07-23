from NetworkSecurity.constant.traning_pipeline import MODEL_FILE_NAME,SAVED_MODEL_DIR
import os
import sys
from sklearn.pipeline import Pipeline
from NetworkSecurity.expection.expection import NetworkSecurityExpection
from NetworkSecurity.logging.logger import logging


class NetworkModel:
    def __init__(self,preprocessor:Pipeline,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise NetworkSecurityExpection(e,sys)
    
    def predict(self,x):
        try:
            x_transformed=self.preprocessor.transform(x)
            y_hat=self.model.predict(x_transformed)
            return y_hat
        except Exception as e:
            return NetworkSecurityExpection(e,sys)