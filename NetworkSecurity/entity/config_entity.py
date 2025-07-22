import os
from datetime import datetime
from NetworkSecurity.constant import traning_pipeline


print(traning_pipeline.PIPELIEN_NAME)
print(traning_pipeline.ARTIFACT_DIR)


class TrainingPipeline:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")   
        self.pipeline_name=traning_pipeline.PIPELIEN_NAME
        self.artifact_name=traning_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.timestam=timestamp


class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipeline):
        self.data_ingestion_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,traning_pipeline.DATA_INGESION_DIR_NAME
        )
        self.feature_store_file_path:str=os.path.join(self.data_ingestion_dir,
                                                      traning_pipeline.DATA_INGESION_FEATURE_STORE_DIR,traning_pipeline.FILE_NAME)
        self.traning_file_path:str=os.path.join(self.data_ingestion_dir,
                                                traning_pipeline.DATA_INGESION_INGESTED_DIR,traning_pipeline.TRAIN_FILE_NAME)
        self.testing_file_path:str=os.path.join(self.data_ingestion_dir,
                                                traning_pipeline.DATA_INGESION_INGESTED_DIR,traning_pipeline.TEST_FILE_NAME)
        
        self.train_test_split_ratio:float=traning_pipeline.DATA_INGESION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name:str=traning_pipeline.DATA_INGESION_COLLECTION_NAME
        self.database_name:str=traning_pipeline.DATA_INGESION_DATABASE_NAME


class DataValidationConfig:
    def __init__(self,traning_pipeline_config:TrainingPipeline):
        self.data_validation_dir:str=os.path.join(traning_pipeline_config.artifact_dir,traning_pipeline.DATA_VALIDATION_DIR_NAME)
        self.vaild_data_dir:str=os.path.join(self.data_validation_dir,traning_pipeline.DATA_VALIDATION_VAILD_DIR)
        self.invalid_dir:str=os.path.join(self.data_validation_dir,traning_pipeline.DATA_VALIDATION_INVAILD_DIR)
        self.valid_train_file_path:str=os.path.join(self.vaild_data_dir,traning_pipeline.TRAIN_FILE_NAME)
        self.valid_test_path:str=os.path.join(self.vaild_data_dir,traning_pipeline.TEST_FILE_NAME)
        self.invlid_train_path:str=os.path.join(self.invalid_dir,traning_pipeline.TRAIN_FILE_NAME)
        self.invlid_test_path:str=os.path.join(self.invalid_dir,traning_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path:str=os.path.join(
            self.data_validation_dir,
            traning_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            traning_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_PATH
        )
class DataTransformationConfig:
    def __init__(self,traning_pipeline_config:TrainingPipeline):
        self.data_transformation_dir:str=os.path.join(traning_pipeline_config.artifact_dir,traning_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path:str=os.path.join(self.data_transformation_dir,traning_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                          traning_pipeline.TRAIN_FILE_NAME.replace('csv',"npy"))
        self.transformed_test_file_path:str=os.path.join(self.data_transformation_dir,traning_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                         traning_pipeline.TEST_FILE_NAME.replace('csv','npy'))
        self.transformed_object_file_path:str=os.path.join(self.data_transformation_dir,traning_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                           traning_pipeline.PREPROCESSING_OBJECT_FILE_NAME)
