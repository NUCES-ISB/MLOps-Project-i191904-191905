from datetime import timedelta
import airflow
import pandas as pd
import numpy as np
import os

from airflow import DAG
from airflow.operators.python import PythonOperator

dag_path = os.getcwd()

def data_cleaning():
    df = pd.read_csv("data.csv")
    df.drop_duplicates(inplace=True)
    df.to_csv("processed_data.csv", index=False)

def cleaned_data_message():
    print("Data successfully cleaned.")

default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': airflow.utils.dates.days_ago(7),
        }

data_cleaning_dag = DAG(
    'data_cleaning_dag',
    default_args=default_args,
    schedule_interval=timedelta(days=30),
    catchup=False
    )


clean_data = PythonOperator(
        task_id='data_cleaning',
        python_callable=data_cleaning,
        dag=data_cleaning_dag
        )

message = PythonOperator(
        task_id='cleaned_data_message',
        python_callable=cleaned_data_message,
        dag=data_cleaning_dag
        )

clean_data >> message
