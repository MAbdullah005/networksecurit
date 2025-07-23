import os
import sys
import mlflow
from NetworkSecurity.expection.expection import NetworkSecurityExpection
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.artifact_entity import ModelTrainerArtifacts,DataTransformationArtifacts
from NetworkSecurity.entity.config_entity import ModelTrainerConfig

from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel
from NetworkSecurity.utils.main_utils.utils import load_object,save_object
from NetworkSecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_model
from NetworkSecurity.utils.ml_utils.metric.classification_metrics import get_classification_score

from sklearn.metrics import r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)

import dagshub
dagshub.init(repo_owner='MAbdullah005', repo_name='networksecurit', mlflow=True)


class Modeltrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
                 data_transformation_config:DataTransformationArtifacts):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_config=data_transformation_config
        except Exception as e:
           raise NetworkSecurityExpection(e,sys)
        
    def track_mlflow(self,best_model,classficationmetrics):
        #mlflow.set_tracking_uri("http://localhost:5000")
        with mlflow.start_run():
            f1_score=classficationmetrics.f1_score
            precision_score=classficationmetrics.precision_score
            recall_score=classficationmetrics.recall_score

            mlflow.log_metric("f1 score",f1_score)
            mlflow.log_metric("precisoin score",precision_score)
            mlflow.log_metric("recall score",recall_score)
            
            mlflow.sklearn.log_model(best_model,"model")

        
    def model_train(self,x_train,y_train,x_test,y_test):
        models={
            "Random Forest":RandomForestClassifier(verbose=1),
            "Decision Tree":DecisionTreeClassifier(),
            "Gradient Boosting":GradientBoostingClassifier(verbose=1),
            "Logistic Regression":LogisticRegression(verbose=1),
            "AdaBoost":AdaBoostClassifier()
        }
        params={
            "Decision Tree":{
            'criterion':['gini','entropy','log_loss'],
            #'splitter':['best','random'],
            #'max_features':['sqrt','log2']
            },
            "Random Forest":{
            #'criterion':['gini','entropy','log_loss'],
            #'max_features':['sqrt','log2',None],
            'n_estimators':[8,16,24,32,64,128,256]
            },
            "Gradient Boosting":{
             #   'loss':['log_loss','exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                #'criterion':['squared_error','friedman_mse'],
                #max_features':['auto','sqrt','log2'],
                "n_estimators": [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.05,.001],
                'n_estimators':[8,16,24,32,64,128,256]
            }
        }
        model_report:dict=evaluate_model(x_train,y_train,x_test,y_test,models,params)

        # to get best model score
        best_model_score=max(sorted(model_report.values()))
        best_model_name=list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model=models[best_model_name]
        x_train_pred=best_model.predict(x_train)
        classification_train_metric=get_classification_score(y_train,x_train_pred)

        # Track the mlflow Experiment  here
        self.track_mlflow(best_model,classification_train_metric)

        y_test_pred=best_model.predict(x_test)
        classification_test_metric=get_classification_score(y_test,y_test_pred)
        self.track_mlflow(best_model,classification_test_metric)
        
        preprocessor=load_object(file_path=self.data_transformation_config.transformed_object_file_path)
        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        network_model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=NetworkModel)

        save_object('final_model/model.pkl',best_model)

        # model trainer artifacts
        model_train_artifacts=ModelTrainerArtifacts(
            trained_model_artifacts=self.model_trainer_config.trained_model_file_path,
            train_metrics_artifacts=classification_train_metric,
            test_metrices_artifacts=classification_test_metric
        )
        logging.info(f"Model train artifacts {model_train_artifacts}")

        return model_train_artifacts
    

        
        
    def initiate_model_trainer(self)->ModelTrainerArtifacts:
        try:
            train_file_path=self.data_transformation_config.transformed_train_file_path
            test_file_path=self.data_transformation_config.transformed_test_file_path

            # laod the training and testing array
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model_train_artifacts=self.model_train(x_train,y_train,x_test,y_test)
            return model_train_artifacts
        except Exception as e:
            raise NetworkSecurityExpection(e,sys)


