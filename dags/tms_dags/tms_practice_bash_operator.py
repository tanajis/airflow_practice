#
# default timeout interval specified
# schedled defined as cron expression
# Both default args and params passed. Check difference

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
import datetime

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id="tms_practice_bash_operator",
    schedule_interval="0 0 * * *",
    start_date=days_ago(2),
    default_args = default_args,
    dagrun_timeout=datetime.timedelta(minutes =60),
    tags=["tms_practice"],
    params={"test": "test"}
) as dag:
    # define dummy operator as start
    start = DummyOperator(
         task_id="start",
         dag=dag,
    )

    # Define End
    end = DummyOperator(
        task_id="end",
        dag=dag,
    )

    # Define task with bash command
    bash_command_ls = BashOperator(
        task_id="bash_command_ls",
        bash_command="ls",
        dag=dag,
    )

    # Define task with bash command
    bash_script = BashOperator(
        task_id="bash_script",
        bash_command="sh test.sh",
        dag=dag,
    )

    # Define Dependencies

    start>>bash_command_ls>>bash_script>>end