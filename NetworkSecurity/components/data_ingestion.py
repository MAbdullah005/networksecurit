from NetworkSecurity.expection.expection import NetworkSecurityExpection
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifacts
from NetworkSecurity.entity.config_entity import DataIngestionConfig
import os
import numpy as np
import sys
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

if not MONGO_DB_URL:
    raise ValueError("❌ MONGO_DB_URL not found. Make sure it's set in your .env file.")


class Dataingestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityExpection(e,sys)
        
    def export_collection_as_dataframe(self):
        """
        read the data deom mongo db which is on cloud mongo atlas 
        
        """
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            if '_df' in df.columns.to_list():
                df=df.drop(columns=['_id'],axis=1)
            df.replace({'na':np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityExpection(e,sys)
        

    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
           feature_store_file_path=self.data_ingestion_config.feature_store_file_path
           # Creating folder
           dir_path=os.path.dirname(feature_store_file_path)
           os.makedirs(dir_path,exist_ok=True)
           dataframe.to_csv(feature_store_file_path,index=False,header=True)
           return dataframe
        except Exception as e:
            NetworkSecurityExpection(e,sys)

    def train_test_split_as_dir(self,dataframe:pd.DataFrame):
        try:
            train_set , test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed the trian test split on dataframe")

            dir_name=os.path.dirname(self.data_ingestion_config.traning_file_path)
            os.makedirs(dir_name,exist_ok=True)
            logging.info("Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.traning_file_path,index=False,header=True)
            train_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            logging.info("Exported train and test file path")
        except Exception as e:
            raise NetworkSecurityExpection(e,sys)
        
        
    def initiate_data_ingested(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.train_test_split_as_dir(dataframe)
            dataingestionartifacts=DataIngestionArtifacts(trained_file_path=self.data_ingestion_config.traning_file_path,
                                                          test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifacts
        except Exception as e:
            raise NetworkSecurityExpection(e,sys)
        

if __name__=="__main__":
    # obj=Dataingestion()
    # obj.export_collection_as_dataframe()
    
   filename = os.path.basename(__file__)   
   print("Current file name:", filename)
   print(os.getcwd())