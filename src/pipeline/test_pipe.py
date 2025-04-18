from src.logging.logger import my_logger
from src.exception.project_exception import MyException

import mlflow
import dagshub
import sys
import pandas as pd
dagshub.init(repo_owner='amankumarchy5423', repo_name='complete-ml-pipeline', mlflow=True)


class test_pipe:
    def __init__(self):
        try :
            pass
        except Exception as e:
            my_logger.error(f"Error in test_pipe class: {str(e)}")
            MyException(e,sys)

    def load_model(self,data):
        try:
            my_logger.info("_____ load_model start ______")

            model_uri = 'runs:/40371064a26146f897fe345111ac81fc/best_model'
            pre_model_uri= 'runs:/44392372c4fc4a4ea15cc8c4481f424d/pre_processor_model'

            ml_model = mlflow.sklearn.load_model(model_uri)
            pre_model = mlflow.sklearn.load_model(pre_model_uri)

            pre_data = pre_model.transform(data)
            my_logger.info("Preprocessed data: {}".format(pre_data))
            my_logger.info("Preprocessed data shape: {}".format(pre_data.shape))

            y_predict = ml_model.predict(pre_data)
            my_logger.info(f"the output is : {y_predict}")

            my_logger.info("_____ load_model end ______")

            return y_predict
        except Exception as e:
            my_logger.error(f"Error in load_model method: {str(e)}")
            MyException(e,sys)


if __name__ == "__main__":
    test_pipe_obj = test_pipe()
    data = pd.DataFrame([1,'Tesla',2016,2.3,'Petrol','Manual',114832,'New',26613.92,'Model X'])
    out = test_pipe_obj.load_model(data)
    print (f" the output is : {out}")
        






