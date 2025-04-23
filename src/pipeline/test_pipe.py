from src.logging.logger import my_logger
from src.exception.project_exception import MyException

import mlflow
# import dagshub
import sys,os
import pandas as pd
import pickle
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from src.cloud.aws_conn import s3client
from src.config.config import test_pipe_config



class test_pipe:
    def __init__(self,s3_conn = s3client(),
                 test_pipe_config = test_pipe_config()):
        try:
            # Load the preprocessor
            self.s3 = s3_conn
            self.config = test_pipe_config

            # Automatically load models
            # self.cloud_model_load()
            
            
        except Exception as e:
            my_logger.error(f"Error in test_pipe class: {str(e)}")
            MyException(e,sys)
    
    def cloud_model_load(self):
        try:
            my_logger.info("____ cloud_model_load start____")
            os.makedirs(self.config.production_model_dir,exist_ok=True)
            my_logger.info("directory created .....")
            
            self.s3.s3_client.download_file(
                Bucket=self.config.bucket_name,
                Key = self.config.s3_pre_model_key_path,
                Filename=self.config.production_pre_model
                )
            self.pre_model = joblib.load(self.config.production_pre_model)
            my_logger.info("production pre_model loaded")

            self.s3.s3_client.download_file(
                Bucket=self.config.bucket_name,
                Key = self.config.s3_model_key_path,
                Filename=self.config.production_ml_model
            )
            self.ml_model = joblib.load(self.config.production_ml_model)
            my_logger.info("production ml_model loade")

            my_logger.info("____ cloud_model_load end____")
        except Exception as e:
            my_logger.error(f"Error in cloud_model_load method: {str(e)}")
            MyException(e,sys)

    def load_model(self,data):
        try:
            my_logger.info("_____ load_model start ______")

            
            my_logger.info(f"Type of self.pre_model: {type(self.pre_model)}")

            pre_data = self.pre_model.transform(data)
            my_logger.info("Preprocessed data: {}".format(pre_data))
            my_logger.info("Preprocessed data shape: {}".format(pre_data.shape))

            pre_data_1 = pd.DataFrame(pre_data)
            pre_data_2 = pre_data_1.iloc[:,:-1]
            y_predict = self.ml_model.predict(pre_data_2)
            my_logger.info(f"the output is : {y_predict}")

            my_logger.info("_____ load_model end ______")

            return y_predict
        except Exception as e:
            my_logger.error(f"Error in load_model method: {str(e)}")
            MyException(e,sys)
            return f"Error: {str(e)}"


if __name__ == "__main__":
    
    test_pipe_obj = test_pipe()
    # data = pd.DataFrame([1,'Tesla',2016,2.3,'Petrol','Manual',114832,'New',26613.92,'Model X'])
    # out = test_pipe_obj.load_model(data)
    # print (f" the output is : {out}")
        






