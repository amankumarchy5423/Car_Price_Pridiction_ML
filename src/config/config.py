from src.utils import my_utils
import os



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
        self.model_accuracy_thresold = 6.52