from src.exception.project_exception import MyException
from src.logging.logger import my_logger

from src.component.data_transformation import DataTransformation
from src.artifact.artifact import data_transformation_artifact
from src.config.config import data_transformation_config

from src.pipeline.train_pipe import TrainPipeline

import sys


def main():
    try:
        my_logger.info("<<< MAIN STARTED >>>")

        obj_train_pipe = TrainPipeline()
        obj_train_pipe.initiate_train_pipe()

        my_logger.info("<<< MAIN ENDTED >>>")
    except Exception as e :
        MyException(e,sys)
        my_logger.error(e)




if __name__ == "__main__":
    main()
