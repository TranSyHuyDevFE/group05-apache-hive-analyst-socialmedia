import pipeline
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='tiktok_data_pipeline',
    default_args=default_args,
    description='A DAG to run TikTok data pipeline',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    scrapper = PythonOperator(
        task_id='scrapper_process',
        python_callable=pipeline.scrapper_process,
    )

    clean_data = PythonOperator(
        task_id='clean_data_process',
        python_callable=pipeline.clean_data_process,
    )

    sentiment_analysis = PythonOperator(
        task_id='sentiment_analysis_process',
        python_callable=pipeline.sentiment_analysis_process,
    )

    sync_to_hive = PythonOperator(
        task_id='sync_data_to_hive_process',
        python_callable=pipeline.sync_data_to_hive_process,
    )

    scrapper >> clean_data >> sentiment_analysis >> sync_to_hive
