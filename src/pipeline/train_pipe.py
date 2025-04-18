from src.exception.project_exception import MyException
from src.logging.logger import my_logger

from src.component.data_transformation import DataTransformation
from src.artifact.artifact import data_transformation_artifact
from src.config.config import data_transformation_config

from src.component.model_training import ModelTrain
from src.config.config import model_train_config

import sys


class TrainPipeline:
    def __init__(self):
        try :
            pass
        except Exception as e:
            my_logger.error(f"Error in TrainPipeline __init__ : {str(e)}")
            MyException(f"Error in TrainPipeline __init__ : {str(e)}",sys) 

    def data_transformation(self):
        try:
            my_logger.info("_____ Data Transformation Started Pipe_____")

            config_obj = data_transformation_config()
        # artifact_obj = data_transformation_artifact()

            data_transformation = DataTransformation(data_transformation_config=config_obj)
            output = data_transformation.initiate_data_transformation()
            return output
        
            my_logger.info("_____ Data Transformation Ended Pipe_____")
        except Exception as e:
            my_logger.error(f"Error in TrainPipeline data_transformation : {str(e)}")
            MyException(f"Error in TrainPipeline data_transformation : {str(e)}",sys)

    def model_train_pipe(self,trans_out):
        try:
            my_logger.info("_____ Model Training Started Pipe_____")
            config_obj = model_train_config()

            model_train = ModelTrain(config=config_obj,artifact=trans_out)
            model_train.initiate_model_train()

            my_logger.info("_____ Model Training Started Pipe_____")
        except Exception as e:
            my_logger.error(f"Error in TrainPipeline model_train_pipe : {str(e)}")
            MyException(f"Error in TrainPipeline model_train_pipe : {str(e)}",sys)


    def initiate_train_pipe(self):
        try:
            my_logger.info("<<<<< Train Pipeline Started >>>>>")
            transformation_out = self.data_transformation()
            my_logger.info("<<< data transformation completed >>>>")

            self.model_train_pipe(trans_out=transformation_out)
            my_logger.info("<<<< Model Training Completed >>>>")


            my_logger.info("<<<<< Train Pipeline Ended >>>>>")
        except Exception as e:
            my_logger.error(f"Error in TrainPipeline initiate_train_pipe : {str(e)}")
            MyException(f"Error in TrainPipeline initiate_train_pipe : {str(e)}",sys)