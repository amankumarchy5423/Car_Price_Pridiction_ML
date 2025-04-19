from src.logging.logger import my_logger
from src.exception.project_exception import MyException

import mlflow
# import dagshub
import sys
import pandas as pd
import pickle
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


class test_pipe:
    def __init__(self):
        try:
            # Load the preprocessor
            self.ml_model = joblib.load('my_model/ml_model.pkl')

            self.pre_model = joblib.load('my_model/preprocessor.pkl')
            
        except Exception as e:
            my_logger.error(f"Error in test_pipe class: {str(e)}")
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
        






