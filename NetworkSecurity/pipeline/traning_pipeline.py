import os
import sys
from NetworkSecurity.expection.expection import NetworkSecurityExpection
from NetworkSecurity.logging.logger import logging

from NetworkSecurity.entity.artifact_entity import (
    DataIngestionArtifacts,
    DataTransformationArtifacts,
    DataValidationArtifacts,
    ModelTrainerArtifacts)


from NetworkSecurity.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    TrainingPipeline
)

from NetworkSecurity.components.data_ingestion import Dataingestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.components.model_trainer import Modeltrainer


class Traning_pipeline:
    def __init__(self):
        self.traning_pipeline=TrainingPipeline()

    def start_data_ingestion(self):
        try:
          logging.info("<<<<<<< Initiate the data ingestion >>>>>>>")
          data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.traning_pipeline)
          data_ingestion=Dataingestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifacts=data_ingestion.initiate_data_ingested()
          logging.info("<<<<<<< Completed the data ingestion >>>>>>>")
          return data_ingestion_artifacts
        
        except Exception as e:
            raise NetworkSecurityExpection(e,sys)
    
    def start_data_validation(self,data_ingestion_artifacts:DataIngestionArtifacts):
        try:
            self.data_ingestion_artifacts=data_ingestion_artifacts
            logging.info("<<<<<<< Initiate the data validation >>>>>>>")
            data_validation_config=DataValidationConfig(
                traning_pipeline_config=self.traning_pipeline)
            
            data_validation=DataValidation(
                data_ingestion_artifacts=self.data_ingestion_artifacts,
                                       data_validation_config=data_validation_config
                                       )
            data_validation_artifacts=data_validation.initiate_data_validation()
            logging.info("<<<<<<< Completed the data validation >>>>>>>")
            return data_validation_artifacts
        
        except Exception as e:
            raise NetworkSecurityExpection(e,sys)
    
    def start_data_transformation(self,data_validaton_artifacts:DataValidationArtifacts):
        try:
          self.data_validaton_artifacts=data_validaton_artifacts
          logging.info("<<<<< Initiate data Transformation <<<<<<<")

          data_transformation_config=DataTransformationConfig(self.traning_pipeline)
          data_transformation=DataTransformation(
              data_validation_artifacts=self.data_validaton_artifacts,
              data_transformation_config=data_transformation_config
                                               )
          data_transformation_artifacts=data_transformation.initiate_data_transformation()
          logging.info("<<<< Completed data Transformation <<<<<<<")
          return data_transformation_artifacts
        
        except Exception as e:
            raise NetworkSecurityExpection(e,sys)

    
    def start_model_traniner(self,data_transformation_artifacts:DataTransformationArtifacts):
        try: 
           self.data_transformation_artifacts=data_transformation_artifacts
           logging.info("<<<<<< Initiate Model trainer and Evaluated stage >>>>>")
           model_trainer_config=ModelTrainerConfig(self.traning_pipeline)

           model_trainer=Modeltrainer(
               model_trainer_config=model_trainer_config,
               data_transformation_config=self.data_transformation_artifacts
               )
           
           model_trainer_artifacts=model_trainer.initiate_model_trainer()

           logging.info("<<<<< Model trainer and Evaluated stage completed >>>>>>")
           return model_trainer_artifacts
        
        except Exception as e:
           raise NetworkSecurityExpection(e,sys)
        

    def run_pipeline(self):
        try:
            data_ingestion_artifacts=self.start_data_ingestion()
            data_validation_artifacts=self.start_data_validation(data_ingestion_artifacts=data_ingestion_artifacts)
            data_transfomation_artifacts=self.start_data_transformation(data_validaton_artifacts=data_validation_artifacts)
            model_traine_artifacts=self.start_model_traniner(data_transformation_artifacts=data_transfomation_artifacts)

            return model_traine_artifacts
        except Exception as e:
            raise NetworkSecurityExpection(e,sys)


if __name__=='__main__':
    obj=Traning_pipeline()
    obj.run_pipeline()


