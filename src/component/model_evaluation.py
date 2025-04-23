from src.config.config import model_evaluation_config
from src.artifact.artifact import model_trainer_artifact,data_transformation_artifact,model_evel_artifact
from src.utils.my_utils.utils import evaluate
from sklearn.metrics import f1_score,r2_score
from src.exception.project_exception import MyException
# from src.constants import TARGET_COLUMN
from src.logging.logger import my_logger
from src.cloud.aws_conn import s3client
# from src.utils.main_utils import load_object
import sys,os
import pandas as pd
from typing import Optional
from src.entity.s3_estimator import Proj1Estimator
from dataclasses import dataclass
import joblib



class ModelEvaluation:

    def __init__(self, model_eval_config: model_evaluation_config, transformation_artifact: data_transformation_artifact,
                 model_trainer_artifact: model_trainer_artifact,
                 cloud_connection : s3client):
        try:
            self.model_eval_config = model_eval_config
            self.data_transformation_artifact = transformation_artifact
            self.trainer_artifact = model_trainer_artifact
            self.s3 = cloud_connection
        except Exception as e:
            raise MyException(e, sys) from e

    def cheack_cloud_model(self) -> bool:
        try:
            my_logger.info("___ check_cloud_model started ___")
            bucket_name = self.s3.s3_resources.Bucket(self.model_eval_config.bucket_name)

            file_objects = [file_object for file_object in bucket_name.objects.filter(Prefix="models/car_price/best_model.pkl")]
            if len(file_objects) > 0 :
                return True
            return False

            my_logger.info("___ check_cloud_model ended ___")
        except Exception as e :
            my_logger.error(e)
            MyException(e,sys)
    def load_cloud_model(self,model_persence : bool) -> None:
        try:
            my_logger.info("___ load_cloud_model started ___")

            if model_persence is True :
                os.makedirs(os.path.dirname(self.model_eval_config.cloud_to_local_path),exist_ok=True)

                self.s3.s3_client.download_file(
                Bucket=self.model_eval_config.bucket_name,
                Key = self.model_eval_config.s3_model_key_path,
                Filename=self.model_eval_config.cloud_to_local_path
                )
                my_logger.info("cloud model loaded into local")
            
            else :
                my_logger.error("bucket can't found, there some thing issue")

            my_logger.info("___ load_cloud_model ended ___")
        except Exception as e:
            my_logger.error(e)
            MyException(e,sys)

    def model_evaluation(self,x_test : pd.DataFrame,model_persence : bool) -> bool:
        try:
            my_logger.info("___ model_evaluation started ___")

            if model_persence is True:

               cloud_model = joblib.load(self.model_eval_config.cloud_to_local_path)
               my_logger.info("cloud model loaded from local dir ")

               x_data = x_test.iloc[:,:-1]
               y_data = x_test.iloc[:,-1]

               cloud_model_ypred = cloud_model.predict(x_data)
               cloud_model_score = evaluate(cloud_model_ypred,y_data)
            # my_logger.info(f"Predictions made local model: {self.model_trainer_artifact.ml_model_f_score}")
               my_logger.info(f"cloud Model evaluation score: {cloud_model_score}")

               if self.trainer_artifact.ml_model_f_score > cloud_model_score :
                   my_logger.info("it means we need to upload our model on cloud")
                   return True
               else :
                   return False
            else:
                my_logger.warning("Cloud model not found, skipping evaluation.")
                my_logger.info("No cloud model present for evaluation.")
                return True

            my_logger.info("___ model_evaluation ended ___")
        except Exception as e :
            my_logger.error(e)
            raise MyException(e,sys)

    def initiate_model_eval(self) -> model_evel_artifact:
        try:
            my_logger.info("___ initiate_model_eval started ___")

            df = pd.read_csv(self.data_transformation_artifact.transformed_test_file)

            model_presence = self.cheack_cloud_model()

            self.load_cloud_model(model_persence=model_presence)

            report = self.model_evaluation(x_test=df,model_persence=model_presence)
            
            return model_evel_artifact(is_model_upload_cloud=report,
                                       cloud_model_path=self.model_eval_config.cloud_to_local_path)

            my_logger.info("___ initiate_model_eval ended ___")
        except Exception as e:
            my_logger.error(e)
            MyException(e,sys)