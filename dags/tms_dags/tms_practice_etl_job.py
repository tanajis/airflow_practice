
import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id="tms_practice_etl_job",
    default_args=default_args,
    description="""This is my first etl job copied from airflow provided workflows""",
    schedule_interval="@daily",
    start_date=days_ago(3),
    tags=["tms_practice"],
) as dag:
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]


    def extract(**kwargs):
        ti = kwargs['ti']
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'

        # Push to xcom
        ti.xcom_push('order_data',data_string)


    def transform(**kwargs):
        ti = kwargs['ti']

        # Pull XCOM data
        extracted_data_string = ti.xcom_pull(task_ids='extract',key='order_data')
        order_data = json.loads(extracted_data_string)

        # Perform calculations
        total_order_value = 0
        for value in order_data.values():
            total_order_value += value

        # Push to XCOM
        total_value = {"total_order_value": total_order_value}
        total_value_json_string = json.dumps(total_value)
        ti.xcom_push('total_order_value', total_value_json_string)

    def load(**args):
        ti = args['ti']
        total_value_string = ti.xcom_pull(task_ids = 'transform',key ='total_order_value')
        total_order_value = json.loads(total_value_string)
        print(total_order_value)

    # Create tasks now which calls extract transform and load

    task_extract = PythonOperator(
        task_id = 'extract',
        python_callable=extract
    )

    task_transform = PythonOperator(
            task_id='transform',
            python_callable=transform
        )
    task_load = PythonOperator(
            task_id='load',
            python_callable=load
        )

    task_extract >> task_transform >> task_load
