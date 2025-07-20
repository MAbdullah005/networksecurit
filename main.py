from NetworkSecurity.components.data_ingestion import Dataingestion
import sys
from NetworkSecurity.expection.expection import NetworkSecurityExpection
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.config_entity import TrainingPipeline

if __name__=="__main__":
    try:
       traningpipelineconfig=TrainingPipeline()
       dataingestionconfig=DataIngestionConfig(traningpipelineconfig)
       data_ingestion=Dataingestion(dataingestionconfig)
       logging.info("Initiate the data ingestion")
       data_ingested_artifacts=data_ingestion.initiate_data_ingested()
       print(data_ingested_artifacts)
    except Exception as e:
        raise NetworkSecurityExpection(e,sys)