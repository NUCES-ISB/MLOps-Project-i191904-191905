import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.neighbors import KNeighborsClassifier
import mlflow
import mlflow.sklearn
import sys
import numpy as np
import pickle


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

def train():
    df = pd.read_csv('processed_data.csv', delimiter=',')

    X = df.drop('normality', axis=1)
    y = df['normality']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.10, random_state=42)

    mlflow.set_experiment("MLOps Project")

    with mlflow.start_run():

        n_neighbors = int(sys.argv[1]) if len(sys.argv) > 1 else 5
        mlflow.log_param("n_neighbors", n_neighbors)

        k_model = KNeighborsClassifier(n_neighbors=n_neighbors)
        model = k_model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        (rmse, mae, r2) = eval_metrics(y_test, predictions)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(model, "knn_model")

        mlflow.end_run()

    pickle.dump(model, open('knn_model.sav', 'wb'))

train()