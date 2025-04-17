from src.exception.project_exception import MyException
from src.logging.logger import my_logger

from src.component.data_transformation import DataTransformation
from src.artifact.artifact import data_transformation_artifact
from src.config.config import data_transformation_config

import sys


def main():
    try:
        my_logger.info("<<< MAIN STARTED >>>")

        config_obj = data_transformation_config()
        # artifact_obj = data_transformation_artifact()
        data_transformation = DataTransformation(data_transformation_config=config_obj)
        data_transformation.initiate_data_transformation()

        my_logger.info("<<< MAIN ENDTED >>>")
    except Exception as e :
        MyException(e,sys)
        my_logger.error(e)




if __name__ == "__main__":
    main()
