from src.logging.logger import my_logger
from src.exception.project_exception import MyException
from src.cloud.aws_conn import s3client
from src.artifact.artifact import model_trainer_artifact,model_evel_artifact
from src.config.config import model_push_config

import os
import boto3
import sys
import joblib


import dagshub
dagshub.init(repo_owner='amankumarchy5423', repo_name='complete-ml-pipeline', mlflow=True)

import mlflow
client = mlflow.MlflowClient()

class ModelPush :
    def __init__(self,s3_conn : s3client,
                 model_train_artifact : model_trainer_artifact,
                 model_push_config : model_push_config,
                 model_eval_artifact : model_evel_artifact
                 ):
        try:
            self.s3 = s3_conn
            self.model_train_artifact = model_train_artifact
            self.config = model_push_config
            self.model_eval_artifact = model_eval_artifact
        except Exception as e :
            my_logger.error(e)
            raise MyException(e,sys)
    
    def push_model_dagshub(self,ml_model,pre_model):
        try:
            with mlflow.start_run():
                mlflow.sklearn.log_model(ml_model,"model",registered_model_name = self.config.ml_model_on_dagshub)
                latest_version = client.get_latest_versions(name = self.config.ml_model_on_dagshub ,stages=['None'])[-1].version
                client.transition_model_version_stage(
                name=self.config.ml_model_on_dagshub,
                version=latest_version,
                stage="Production",
                archive_existing_versions=True
                  )
            my_logger.info("model pushed on dagshub")

            
            mlflow.sklearn.log_model(pre_model,"model",registered_model_name = "preprocessor")
            latest_version = client.get_latest_versions(name = 'preprocessor',stages=['None'])[-1].version
            client.transition_model_version_stage(
            name="preprocessor",
            version=latest_version,
            stage="Production",
            archive_existing_versions=True
                  )
            # mlflow.end_run()
            mlflow.end_run() 
        except Exception as e :
            my_logger.error(e)
            raise MyException(e,sys)
         
    def push_model_aws(self,model,pre_model):
        try:
            my_logger.info("___ push_model_aws startes ___")

            self.s3.s3_client.upload_file(self.model_train_artifact.ml_model_path, self.config.bucket_name, self.config.s3_model_key_path)
            self.s3.s3_client.upload_file(self.model_train_artifact.pre_model_path,self.config.bucket_name,self.config.s3_pre_model_key_path)
            
            my_logger.info("model uploaded to AWS S3")

            my_logger.info("___ push_model_aws ends ___")
        except Exception as e :
            my_logger.error(e)
            raise MyException(e,sys)
    
    def initiate_model_pushining(self):
        try:
            my_logger.info("____ initiate_model_pushing started ____")
            ml_model = joblib.load(self.model_train_artifact.ml_model_path)
            pre_model = joblib.load(self.model_train_artifact.pre_model_path)

            # if self.model_eval_artifact.is_model_upload_cloud is True :
            #    my_logger.info("all model are uploaded to cloud .....")
            self.push_model_dagshub(ml_model,pre_model)
            self.push_model_aws(ml_model,pre_model)
            
            # else:
            #     my_logger.info("Model upload to cloud is not required.")

            my_logger.info("____ initiate_model_pushing ended ____")
        
        except Exception as e:
            my_logger.error(e)
            raise MyException(e,sys)
        


# if __name__ == '__main__':
#     obj = model_push()
#     obj.initiate_model_pushining()

