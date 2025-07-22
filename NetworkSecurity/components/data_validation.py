from NetworkSecurity.entity.artifact_entity import DataIngestionArtifacts,DataValidationArtifacts
from NetworkSecurity.entity.config_entity import DataValidationConfig
from NetworkSecurity.expection.expection import NetworkSecurityExpection
from NetworkSecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from NetworkSecurity.constant.traning_pipeline import SCHEMA_FILE_PATH
from NetworkSecurity.logging.logger import logging
import os
import sys
from scipy.stats import ks_2samp
import pandas as pd


class DataValidation:
    def __init__(self,data_ingestion_artifacts:DataIngestionArtifacts,
                 data_validation_config:DataValidationConfig):
        try:
    
           self.data_ingestion_artifacts=data_ingestion_artifacts
           self.data_validation_config=data_validation_config
           self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityExpection(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            NetworkSecurityExpection(e,sys)

    def validate_no_of_column(self,dataframe:pd.DataFrame):
        try:
            number_of_column=self._schema_config
            logging.info(f"required number of column {number_of_column}")
            logging.info(f"Data frame has column {len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_column:
                return True
            return False
        except Exception as e:
            NetworkSecurityExpection(e,sys)

    def detect_dataset_drift(self,basedf:pd.DataFrame,currentdf:pd.DataFrame,threshhold=0.05,)->bool:
        try:
            status=True
            report={}
            for column in basedf.columns:
                d1=basedf[column]
                d2=currentdf[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshhold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    status=False
                    is_found=True
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                }})

                # Create the directory
                drift_report_file_path=self.data_validation_config.drift_report_file_path
                dir_path=os.path.dirname(drift_report_file_path)
                os.makedirs(dir_path,exist_ok=True)
                write_yaml_file(file_path=drift_report_file_path,content=report)


        except Exception as e:
            NetworkSecurityExpection(e,sys)
        
    def initiate_data_validation(self)->DataValidationArtifacts:
        try:

            train_file_path=self.data_ingestion_artifacts.trained_file_path
            test_file_path=self.data_ingestion_artifacts.test_file_path

            ## read the data from train and test
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

            # validate the number of columns 
            status=self.validate_no_of_column(train_dataframe)
            if not status:
                error_message=f"Train dataset does not contain all column\n"
            status=self.validate_no_of_column(test_dataframe)
            if not status:
                error_message=f"test dataset does not contain all column\n"

            required_column=self._schema_config["numerical_columns"]
            train_column=train_dataframe.columns
            test_column=test_dataframe.columns

            if not all(col in train_column for col in required_column):
               error_message = "Train dataset does not contain all required numerical columns"
               raise NetworkSecurityExpection(error_message, sys)
            
            if not all(col in test_column for col in required_column):
               error_message = "Test dataset does not contain all required numerical columns"
               raise NetworkSecurityExpection(error_message, sys)



            # let check data drift
            status=self.detect_dataset_drift(basedf=train_dataframe,currentdf=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,header=True,index=False
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_path,index=False,header=True
            )

            data_validation_artifacts=DataValidationArtifacts(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path

            )
            return data_validation_artifacts
        except Exception as e:
            raise NetworkSecurityExpection(e,sys)

