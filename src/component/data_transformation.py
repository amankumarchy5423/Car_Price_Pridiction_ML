from src.logging.logger import my_logger
from src.exception.project_exception import MyException
from src.config.config import data_transformation_config
from src.artifact.artifact import data_transformation_artifact


import os
import sys
import pandas as pd
import numpy as np
import joblib
import yaml
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline,make_pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer,KNNImputer





class DataTransformation:
    def __init__(self, data_transformation_config : data_transformation_config ):
                #  artifact : data_transformation_artifact):
        try :
            self.config = data_transformation_config
            # self.artifact = artifact
        except Exception as e:
            my_logger.error(f"Error in DataTransformation class: {str(e)}")
            MyException(e,sys)

    def data_seperation(self,data:pd.DataFrame)->pd.DataFrame:
        try:
            my_logger.info("_____ data_seperation started ______")

            
            my_logger.info("in data we differenciate at dependent and independent variable .")

            train_data,test_data = train_test_split(data,train_size=0.8)
            my_logger.info("data is split into train and test .")

            my_logger.info("_____ data_seperation ended ______")
            return train_data,test_data

        except Exception as e:
            my_logger.error(f"Error in data_seperation method: {str(e)}")
            MyException(e,sys)

    def load_column(self)->list:
        try:
            my_logger.info("_____ load_column started ______")

            with open(self.config.column_yaml,'r') as file:
                column = yaml.safe_load(file)
            # column = yaml.safe_load(os.path(self.config.column_yaml))
                my_logger.info(f"column is loaded .{column}")

                categorical_colm = column['categorical']
                numerical_col = column['numerical']
                output_col = column['output']
                my_logger.info(f"column is loaded .{categorical_colm} {numerical_col}")

                return categorical_colm,numerical_col,output_col

            my_logger.info("_____ load_column ended ______")
        except Exception as e:
            my_logger.error(f"Error in load_column method: {str(e)}")
            MyException(e,sys)

    def build_preprocessor(self,categorical_col,numerical_col,output_col,train_data) ->None:
        try:
            my_logger.info("_____ data_preprocessing started ______")

            num_pipeline : Pipeline = Pipeline([
            ('num_impute', KNNImputer(n_neighbors=5)),
            ('num_scale', StandardScaler())
            ])

            cat_pipeline : Pipeline = Pipeline([
            ('cat_impute', SimpleImputer(strategy='most_frequent')),  # KNNImputer won't work on non-numeric
            ('cat_encode', OneHotEncoder(handle_unknown='ignore',sparse_output = False))
            ])

            output_pipeline = Pipeline([
                ('output_impute', SimpleImputer(strategy='mean'))])  # KNNIm

            preprocessor : ColumnTransformer = ColumnTransformer(transformers=[
            ('num', num_pipeline, numerical_col),
            ('cat', cat_pipeline, categorical_col),
            ('output',output_pipeline, output_col)
            ])
            my_logger.info("preprocessing pipeline is created .")

            input_columns : list= categorical_col + numerical_col + output_col
            my_logger.info(f'ianput column ::::{input_columns}')
            my_logger.info(f'train data ::{type(train_data)}:::\n{train_data.head()}')

            if not isinstance(train_data, pd.DataFrame):
                train_data : pd.DataFrame= pd.DataFrame(train_data)
                my_logger.info(f'data is not a dataframe {train_data.head()}')

            preprocessor.fit(train_data[input_columns])
            my_logger.info("preprocessing pipeline is fitted.")

            os.makedirs(os.path.dirname(self.config.preprocessor_model),exist_ok=True)
            joblib.dump(preprocessor,self.config.preprocessor_model)

            my_logger.info("preprocessor model is dumped ...")
            




            my_logger.info("_____ data_preprocessing ended ______")
        except Exception as e:
            my_logger.error(e)
            MyException(e,sys)

    def transformed_data(self,train_data,test_data) -> None:
        try:
            my_logger.info("_____ transformed_data started ______")

            preprocessor = joblib.load(self.config.preprocessor_model)
            my_logger.info("preprocessor model is loaded ...")

            columns : list = [col for col in train_data.columns ]
            my_logger.info(f"columns are selected .{columns}")

            # pre_model = preprocessor.fit(train_data[columns])
            my_logger.info(f"preprocessor model is fitted ...{preprocessor}")
            my_logger.info(f"train data type is {type(train_data)}")
            # train_data = pd.DataFrame(train_data)
            # test_data = pd.DataFrame(test_data)

            transformed_train_data : np.array = preprocessor.transform(train_data)
            transformed_test_data : np.array = preprocessor.transform(test_data)
            my_logger.info(f"transformed data is created ...{transformed_train_data.shape}")

            transformed_train_data_df : pd.DataFrame = pd.DataFrame(transformed_train_data)
            # transformed_train_data_df['Price'] = train_data['Price']

            transformed_test_data_df : pd.DataFrame = pd.DataFrame(transformed_test_data)
            # transformed_test_data_df['Price'] = test_data['Price']

            os.makedirs(os.path.dirname(self.config.train_transform_data),exist_ok=True)
            transformed_train_data_df.to_csv(self.config.train_transform_data,index=False)
            my_logger.info(f"transformed train data is saved ...{self.config.train_transform_data}")

            os.makedirs(os.path.dirname(self.config.test_transform_data),exist_ok=True)
            transformed_test_data_df.to_csv(self.config.test_transform_data,index=False)
            my_logger.info(f"transformed test data is saved ...{self.config.test_transform_data}")

            
            


            my_logger.info("_____ transformed_data ended ______")
        except Exception as e :
            my_logger.error(e)
            MyException(e,sys)

    def initiate_data_transformation(self) -> None:
        try:
            my_logger.info("_____ initiate_data_transformation started ______")

            data : pd.DataFrame= pd.read_csv("C:/Users/HP/Downloads/car_price_prediction_.csv")
            my_logger.info("data is loaded .",data.head())

            train,test = self.data_seperation(data=data)

            cat,num,out = self.load_column()
            my_logger.info(f"cat columns are {train[cat]} , num columns are {num} ")

            self.build_preprocessor(categorical_col=cat,numerical_col=num,output_col=out,train_data=train.iloc[:,:])

            self.transformed_data(train_data=train,test_data=test)

            my_logger.info("_____ initiate_data_transformation ended ______")

            return data_transformation_artifact(transformed_train_file=self.config.train_transform_data,
                                                transformed_test_file=self.config.test_transform_data,
                                                pre_model_path=self.config.preprocessor_model)

            
        except Exception as e:
            my_logger.error(f"Error in initiate_data_transformation method: {str(e)}")
            MyException(e,sys)