from dataclasses import dataclass
from pathlib import Path



@dataclass
class data_ingestion:
    data_ingestion_artifact : str

@dataclass
class data_transformation_artifact:
    transformed_train_file : str
    transformed_test_file : str
    pre_model_path : str


@dataclass
class model_trainer_artifact:
    ml_model_path : str
    pre_model_path : str
    ml_model_f_score : float

@dataclass
class model_evel_artifact:
    is_model_upload_cloud : bool
    cloud_model_path : str