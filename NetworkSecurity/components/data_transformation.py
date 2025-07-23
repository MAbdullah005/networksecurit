import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from NetworkSecurity.constant.traning_pipeline import TARGET_COLUMN
from NetworkSecurity.constant.traning_pipeline import DATA_TRANSFORMED_IMPUTER_PARAMS

from NetworkSecurity.entity.artifact_entity import (
    DataTransformationArtifacts,
    DataValidationArtifacts
    )

from NetworkSecurity.expection.expection import NetworkSecurityExpection
from NetworkSecurity.entity.config_entity import DataTransformationConfig
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,data_validation_artifacts:DataValidationArtifacts,
                 data_transformation_config:DataTransformationConfig):
        try:

            self.data_validation_artifacts:DataValidationArtifacts=data_validation_artifacts
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:

            NetworkSecurityExpection(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:

            return pd.read_csv(file_path)
        except Exception as e:
            NetworkSecurityExpection(e,sys)

    def get_data_transformed_obj(self)->Pipeline:
        """
        inititate the KNN imputer with specifaic parameter from 
        training pipeline and return the transoformed object
        """

        logging.info("Entered the get_data_transformed_obj method of transformation class")
        try:
            logging.info("step 1 . 1")
            imputer=KNNImputer(**DATA_TRANSFORMED_IMPUTER_PARAMS)
            logging.info("step 1.2")
            logging.info(
                f"inilize KNNimputer with {DATA_TRANSFORMED_IMPUTER_PARAMS}"
            )
            logging.info("step 1.3")
            processor=Pipeline([('imputer',imputer)])
            logging.info("step 1.4")
            return processor
        except Exception as e:
            NetworkSecurityExpection(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifacts:

        logging.info("Initiate data trnsformation method of class DataTransformation")
        try:
            logging.info("Start Data Transofrmation Step")

            train_df=DataTransformation.read_data(self.data_validation_artifacts.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifacts.valid_test_file_path)
            logging.info("step 1")
            # Traning dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)
            logging.info("step 2")

            # testing dataframe
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)
            logging.info("step 3")

            # transformed the data with pipeline
            preprocessor=self.get_data_transformed_obj()
       
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_train_input_feature=preprocessor_object.transform(input_feature_train_df)
            transformed_test_input_feature=preprocessor_object.transform(input_feature_test_df)
            logging.info("step 4")

            train_arr=np.c_[transformed_train_input_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_test_input_feature,np.array(target_feature_test_df)]
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,obj=preprocessor_object)

            save_object('final_model/preprocessor.pkl',preprocessor_object)
            logging.info("step 5")

            # Data transformation artifacts
            data_transformation_artifacts=DataTransformationArtifacts(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            logging.info("step 5")
            logging.info("finish data transformation steps")
            return data_transformation_artifacts

        except Exception as e:
            NetworkSecurityExpection(e,sys)
