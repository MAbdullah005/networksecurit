from NetworkSecurity.components.data_ingestion import Dataingestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.components.model_trainer import Modeltrainer
import time
import sys
from NetworkSecurity.expection.expection import NetworkSecurityExpection
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.config_entity import TrainingPipeline
from NetworkSecurity.entity.artifact_entity import DataValidationArtifacts,DataTransformationArtifacts
from NetworkSecurity.entity.config_entity import DataValidationConfig,DataTransformationConfig,ModelTrainerConfig

if __name__=="__main__":
    try:
       start=time.time()
       traningpipelineconfig=TrainingPipeline()
       dataingestionconfig=DataIngestionConfig(traningpipelineconfig)
       data_ingestion=Dataingestion(dataingestionconfig)
       logging.info("<<<<<<< Initiate the data ingestion >>>>>>>")
       data_ingested_artifacts=data_ingestion.initiate_data_ingested()
       print(data_ingested_artifacts)
       logging.info("<<<<<<<< Data Ingestion Completed >>>>>>")
      
       data_validation_config=DataValidationConfig(traningpipelineconfig)
       data_validation=DataValidation(data_ingested_artifacts,data_validation_config)
       logging.info("<<<<<< Initeate Data Validation >>>>>>")
       data_validation_artifacts=data_validation.initiate_data_validation()
       logging.info("<<<<< Data Validation Completed")
       print(data_validation_artifacts)

       logging.info("<<<<< stated Data Trnsformation >>>>>")
       data_transformation_config=DataTransformationConfig(traningpipelineconfig)
       data_transformation=DataTransformation(data_validation_artifacts,data_transformation_config)
       data_transformation_artifacts=data_transformation.initiate_data_transformation()
       logging.info("<<<<<<< completed Data transformation >>>>>>>")
       print(data_transformation_artifacts)

       logging.info(">>>>>> Model Traning  Started <<<<<<")
       model_train_config=ModelTrainerConfig(traningpipelineconfig)
       model_trainer=Modeltrainer(model_trainer_config=model_train_config,data_transformation_config=data_transformation_artifacts)
       model_train_artifact=model_trainer.initiate_model_trainer()

       logging.info(f"<<<<<< Model Traning  Completed >>>>>")
       end=time.time()
       print(f"Execution time: {end - start:.2f} seconds")
       logging.info(f"Execution time: {end - start:.2f} seconds")

    except Exception as e:
        raise NetworkSecurityExpection(e,sys)