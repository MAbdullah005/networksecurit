from NetworkSecurity.components.data_ingestion import Dataingestion
from NetworkSecurity.components.data_validation import DataValidation
import sys
from NetworkSecurity.expection.expection import NetworkSecurityExpection
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.config_entity import TrainingPipeline
from NetworkSecurity.entity.artifact_entity import DataValidationArtifacts
from NetworkSecurity.entity.config_entity import DataValidationConfig

if __name__=="__main__":
    try:
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

    except Exception as e:
        raise NetworkSecurityExpection(e,sys)