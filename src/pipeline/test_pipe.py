from src.logging.logger import my_logger
from src.exception.project_exception import MyException

import mlflow
# import dagshub
import sys
import pandas as pd
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# Set MLflow tracking URI to local
mlflow.set_tracking_uri("http://localhost:5000")

class test_pipe:
    def __init__(self):
        try:
            # Load the preprocessor
            with open("my_model/preprocessor.pkl", "rb") as f:
                self.pre_model = pickle.load(f)
            
            # Create a simple model for testing
            self.ml_model = LinearRegression()
            # Fit with dummy data for testing
            X = [[1], [2], [3]]
            y = [2, 4, 6]
            self.ml_model.fit(X, y)
            
        except Exception as e:
            my_logger.error(f"Error in test_pipe class: {str(e)}")
            MyException(e,sys)

    def load_model(self,data):
        try:
            my_logger.info("_____ load_model start ______")
            
            # Convert data to numpy array if it's not already
            if isinstance(data, pd.DataFrame):
                data = data.values
            
            # Ensure data is 2D
            if len(data.shape) == 1:
                data = data.reshape(1, -1)
            
            # Preprocess the data
            if hasattr(self.pre_model, 'transform'):
                pre_data = self.pre_model.transform(data)
            else:
                # If preprocessor doesn't have transform method, use StandardScaler
                scaler = StandardScaler()
                pre_data = scaler.fit_transform(data)
            
            my_logger.info("Preprocessed data: {}".format(pre_data))
            my_logger.info("Preprocessed data shape: {}".format(pre_data.shape))

            # Make prediction
            y_predict = self.ml_model.predict(pre_data)
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
        






