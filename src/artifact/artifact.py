from dataclasses import dataclass
from pathlib import Path



@dataclass
class data_ingestion:
    data_ingestion_artifact : str

@dataclass
class data_transformation_artifact:
    transformed_train_file : str
    transformed_test_file : str