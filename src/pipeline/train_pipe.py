from src.exception.project_exception import MyException
from src.logging.logger import my_logger

from src.component.data_transformation import DataTransformation
from src.artifact.artifact import data_transformation_artifact
from src.config.config import data_transformation_config

from src.component.model_training import ModelTrain
from src.config.config import model_train_config
from src.artifact.artifact import model_trainer_artifact

from src.config.config import model_evaluation_config
from src.artifact.artifact import model_evel_artifact
from src.component.model_evaluation import ModelEvaluation

from src.component.model_push import ModelPush
from src.config.config import model_push_config

from src.cloud.aws_conn import s3client

import sys


class TrainPipeline:
    def __init__(self):
        try :
            pass
        except Exception as e:
            my_logger.error(f"Error in TrainPipeline __init__ : {str(e)}")
            MyException(f"Error in TrainPipeline __init__ : {str(e)}",sys) 

    def data_transformation(self) -> data_transformation_artifact:
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

    def model_train_pipe(self,trans_out : data_transformation_artifact) -> model_trainer_artifact:
        try:
            my_logger.info("_____ Model Training Started Pipe_____")
            config_obj = model_train_config()

            model_train = ModelTrain(config=config_obj,artifact=trans_out)
            model_train_output = model_train.initiate_model_train()

            return model_train_output

            my_logger.info("_____ Model Training Started Pipe_____")
        except Exception as e:
            my_logger.error(f"Error in TrainPipeline model_train_pipe : {str(e)}")
            MyException(f"Error in TrainPipeline model_train_pipe : {str(e)}",sys)
    
    def model_eval_pipe(self,train_out : model_trainer_artifact,transformation_artifact : data_transformation_artifact) -> model_evel_artifact :
        try :
            my_logger.info("_____ Model Evaluation Started Pipe_____")
            config_obj = model_evaluation_config()

            s3_client_obj = s3client()

            model_eval_obj = ModelEvaluation(model_eval_config=config_obj,
                                         model_trainer_artifact=train_out,
                                         transformation_artifact=transformation_artifact,
                                         cloud_connection=s3client)
            my_logger.info('ModelEvaluation class starts')

            model_eval_out = model_eval_obj.initiate_model_eval()

            my_logger.info("_____ Model Evaluation ended Pipe_____")
        except Exception as e :
            my_logger.error(f"Error in TrainPipeline model_eval_pipe : {str(e)}")
            MyException(e,sys)

    
    def model_push_pipe(self,model_train_output : model_trainer_artifact,model_eval_out : model_evel_artifact):
        try:
            my_logger.info("_____ Model Push Started Pipe_____")

            model_push_config_obj = model_push_config()

            s3_client_obj = s3client()

            model_push_obj = ModelPush(s3_conn=s3_client_obj,
                                       model_push_config=model_push_config_obj,
                                       model_train_artifact=model_train_output,
                                       model_eval_artifact=model_eval_out)
            
            model_push_obj.initiate_model_pushining()

            my_logger.info("_____ Model Push Ended Pipe_____")
        except Exception as e :
            my_logger.error(e)
            raise MyException(e,sys)


    def initiate_train_pipe(self):
        try:
            my_logger.info("<<<<< Train Pipeline Started >>>>>")
            transformation_out = self.data_transformation()
            my_logger.info("<<< data transformation completed >>>>")

            model_train_out = self.model_train_pipe(trans_out=transformation_out)
            my_logger.info("<<<< Model Training Completed >>>>")

            model_eval_out = self.model_eval_pipe(train_out=model_train_out,
                                                  transformation_artifact=transformation_out)
            my_logger.info("<<<< Model Evaluation Completed >>>>>")

            self.model_push_pipe(model_train_output=model_train_out,model_eval_out=model_eval_out)
            my_logger.info("<<< Model Push Completed >>>>")

            # self.model_push_pipe(model_train_output=)

            my_logger.info("<<<<< Train Pipeline Ended >>>>>")
        except Exception as e:
            my_logger.error(f"Error in TrainPipeline initiate_train_pipe : {str(e)}")
            MyException(f"Error in TrainPipeline initiate_train_pipe : {str(e)}",sys)