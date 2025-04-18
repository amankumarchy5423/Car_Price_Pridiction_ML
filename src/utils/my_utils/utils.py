import numpy as np
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score



def evaluate(y_actual,y_predict):
    matrix = {
        'rmse' : np.sqrt(mean_squared_error(y_true=y_actual,y_pred=y_predict)),
        'mae' : mean_absolute_error(y_actual,y_predict),
        'r2' : r2_score(y_actual,y_predict)
    }
    print(f"Metrics: {matrix['r2']}")
    return sum(matrix.values())