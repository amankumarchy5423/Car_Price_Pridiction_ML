from src.utils import my_utils
import os
from datetime import datetime



class data_transformation_config:
    def __init__(self):
        self.train_transform_data : str = os.path.join(
            my_utils.ARTIFACT_DIR,
            my_utils.DATA_TRANSFORMATION_DIR,
            my_utils.TRAIN_FILE
        )
        self.test_transform_data : str = os.path.join(
            my_utils.ARTIFACT_DIR,
            my_utils.DATA_TRANSFORMATION_DIR,
            my_utils.TEST_FILE
        )
        self.preprocessor_model :str = os.path.join(
            my_utils.MODEL_DIR,
            my_utils.PREPEOCESSOR_MODEL
        )
        self.column_yaml :str = 'columns.yaml'


class model_train_config:
    def __init__(self):
        self.model_train_dir : str = os.path.join(my_utils.ARTIFACT_DIR,
                                                  my_utils.MODEL_TRAIN_DIR)
        self.param_dir : str = os.path.join(self.model_train_dir,'model_param.yaml')
        self.model_accuracy_thresold : float = 6.52
        self.ml_model_path : str = os.path.join(my_utils.MODEL_DIR,my_utils.ML_MODEL_FILE)

class model_evaluation_config:
    def __init__(self):
        self.bucket_name : str = my_utils.MODEL_S3_BUCKET_NAME
        self.s3_model_key_path : str = my_utils.MODEL_PUSHER_S3_KEY
        self.cloud_to_local_path : str = os.path.join(my_utils.CLOUD_TO_LOCAL_MODEL_DIR,
                                                      my_utils.CLOUD_TO_LOCAL_MODEL_FILE)
        
class model_push_config:
    def __init__(self):
        self.ml_model_on_dagshub : str = os.path.join(my_utils.ML_MODEL_NAME_ON_DAGSHUB)
        self.bucket_name : str = my_utils.MODEL_S3_BUCKET_NAME
        self.s3_model_key_path : str = my_utils.MODEL_PUSHER_S3_KEY
        self.s3_pre_model_key_path : str = my_utils.PREMODEL_PUSHER_S3_KEY

class test_pipe_config :
    def __init__(self):
        
        self.bucket_name : str = my_utils.MODEL_S3_BUCKET_NAME
        self.s3_model_key_path : str = my_utils.MODEL_PUSHER_S3_KEY
        self.s3_pre_model_key_path : str = my_utils.PREMODEL_PUSHER_S3_KEY
        self.production_model_dir : str = my_utils.PRODUCTION_MODEL_DIR
        self.production_ml_model : str = os.path.join(self.production_model_dir,my_utils.TEST_PIPE_ML_MODEL_FILE)
        self.production_pre_model : str = os.path.join(self.production_model_dir,my_utils.TEST_PIPE_PRE_MODEL_FILE)



