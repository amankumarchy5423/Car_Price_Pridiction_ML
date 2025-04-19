from src.logging.logger import my_logger
from src.exception.project_exception import MyException
from src.utils.my_utils.utils import evaluate
from src.config.config import model_train_config
from src.artifact.artifact import data_transformation_artifact

import pandas as pd
import numpy as np
import yaml
import joblib
import os,sys

from sklearn.linear_model import LinearRegression,ElasticNet,Ridge,Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV

from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_error
from sklearn.model_selection import train_test_split


import dagshub
dagshub.init(repo_owner='amankumarchy5423', repo_name='complete-ml-pipeline', mlflow=True)

import mlflow
client = mlflow.MlflowClient()


class ModelTrain :
    def __init__(self,config:model_train_config,artifact:data_transformation_artifact):
        try:
            self.config = config
            self.artifact = artifact
        except Exception as e:
            my_logger.error(f"Error in ModelTrain class : {str(e)}")
            MyException(f"Error in ModelTrain class : {str(e)}",sys)

    def model_train(self,train_data : pd.DataFrame)-> None :
        try:
            my_logger.info("_____ Model Train Started_____")

            x_data = train_data.iloc[:,:-1]
            y_data = train_data.iloc[:,-1]
            x_train,x_test,y_train,y_test = train_test_split(x_data,y_data,train_size=0.8)
            my_logger.info("_____ Data Split Done_____")

            models = {
             'LR' : LinearRegression(),
             'Lasso' : Lasso(),
             'Ridge' : Ridge(),
             'ElasticNet' : ElasticNet(),
             'DecisionTree' : DecisionTreeRegressor(),
             'RandomForest' : RandomForestRegressor(),
             'SVR' : SVR(),
             'GradientBoosting' : GradientBoostingRegressor(),
    
             }
            params = {
                'LR':{
                    'fit_intercept' : [True]},
                'Lasso' : {
        'alpha' :[1,3],
        'max_iter' : [1000,1200]
    },
    'Ridge' : {
        'alpha' : [1,5],
    },
    'ElasticNet' : {
        'alpha' : [1,3],
        'l1_ratio' : [0.5,0.7]
    },
    'DT' : {
        'max_depth' : [5,6],
        'criterion' : ['squared_error','absolute_error'],
        'max_leaf_nodes' : [10,20]
    },
    'RF' : {
        'n_estimators' : [10,20],
        'criterion' : ['squared_error','absolute_error'],
        'max_depth' : [4,5]
    },
    'SVM' : {
        'kernel' : ['poly', 'rbf', 'sigmoid'],
        'gamma' : ['scale', 'auto'],
        'verbose' : [True] 
    },
    'GBM' : {}
}

            my_logger.info("_____ Model Parameters Loaded_____")

            best_score = self.config.model_accuracy_thresold
            best_model = None
            best_model_name = None
            best_run_id = None

            for i in range(len(models)):
                model = list(models.values())[i]
                model_name = list(models.keys())[i]
                model_params = params.get(model_name, {})

                with mlflow.start_run(run_name=f"{model_name}_parent_run") as parent_run:
                    grid = GridSearchCV(model, model_params, cv=5,verbose=2)
                    grid.fit(x_train, y_train)

                    for j in range(len(grid.cv_results_['params'])):
                        with mlflow.start_run(run_name=f"{model_name}_child_run", nested=True) as child_run:
                            my_logger.info("model_name", model_name)

                            for param_name, param_value in grid.cv_results_['params'][j].items():
                                mlflow.log_param(param_name, param_value)

                            y_pred = grid.predict(x_test)
                            accuracy = evaluate(y_test, y_pred)
                            mlflow.log_metric("accuracy", accuracy)
                            my_logger.info(f"name of model{model_name} and accuracy {accuracy}")

                            if accuracy > best_score:
                                best_score = accuracy
                                best_model = grid.best_estimator_
                                best_model_name = model_name
                                best_run_id = child_run.info.run_id
                                my_logger.info(f"Save if this is the best model so far{best_model_name}")

                joblib.dump(best_model,'my_model/ml_model.pkl')


            if best_run_id is None:
                raise MyException("No model met the accuracy threshold; nothing to register.", sys)

# model_uri = f"runs:/{best_run_id}/model"

            model_uri = f"runs:/{best_run_id}/model"
            registered_model_name = "Best-ml-model"
            my_logger.info("registering best model in model registery....")

            mlflow.register_model(model_uri=model_uri, name=registered_model_name)

# Get all versions of this registered model
            all_versions = client.search_model_versions(f"name='{registered_model_name}'")


            # latest_version = client.get_latest_versions(name=registered_model_name, stages=["None"])[0].version

            # client.transition_model_version_stage(
            # name=registered_model_name,
            # version=latest_version,
            # stage="Production",
            # archive_existing_versions=True )
            latest_version = sorted(all_versions, key=lambda x: int(x.version))[-1].version

# Promote to Production and archive older versions
            client.transition_model_version_stage(
             name=registered_model_name,
             version=latest_version,
             stage="Production",
             archive_existing_versions=True
             )
            my_logger.info(f" {best_model_name} with accuracy {best_score} promoted to Production!")

            my_logger.info("______Model Training and Evaluation Complete______")
        except Exception as e:
             my_logger.error(f"Error in model training and evaluation: {e}")
             MyException(e,sys)
    

    def initiate_model_train(self):
        try:
            my_logger.info("_____initiate Model Train started_____")
            train_data = pd.read_csv(self.artifact.transformed_train_file)
            test_data = pd.read_csv(self.artifact.transformed_test_file)
            my_logger.info(f"data_loaded...and empty report {train_data.isnull().sum()}")

            self.model_train(train_data=train_data)
            my_logger.info("model trained...")


            my_logger.info("_____ initate Model Train ended_____")
        except Exception as e:
            my_logger.error(f"Error in model_train method : {str(e)}")
            MyException(f"Error in model_train method : {str(e)}",sys)


