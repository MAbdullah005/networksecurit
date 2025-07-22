import os
import sys
import pandas as pd
import numpy as np

"""
Defining common constant variable for traning pipeline

"""
TARGET_COLUMN="Result"
PIPELIEN_NAME:str="NetworkSecurity"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str="PhisingData.csv"

TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"

SCHEMA_FILE_PATH:str=os.path.join("data_schema","schema.yaml")



"""
Data Ingestion related constants start DATA_INGESTION VAR name
"""

DATA_INGESION_COLLECTION_NAME:str ="NetworkData"
DATA_INGESION_DATABASE_NAME:str ="Abdullah"
DATA_INGESION_DIR_NAME:str ="data_ingestion"
DATA_INGESION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESION_INGESTED_DIR:str="ingested"
DATA_INGESION_TRAIN_TEST_SPLIT_RATIO:float=0.2


"""
Data validation related constant start with Data_validation var name
"""

DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VAILD_DIR:str="validated"
DATA_VALIDATION_INVAILD_DIR:str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_PATH:str="report.yaml"
