from dataclasses import dataclass
from pathlib import Path



@dataclass
class data_ingestion:
    data_ingestion_artifact : str

@dataclass
class data_transformation_artifact:
    data_transformation_artifact : str
    preprocessor_model : str