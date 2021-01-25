
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow'
}


with DAG(
    dag_id='tms_practice_task_group',
    default_args=args,
    start_date=days_ago(3),
        schedule_interval=None,
        tags=['tms-practice'],) as dag:

    start = DummyOperator(
        task_id='start',
        dag=dag
    )

    end = DummyOperator(
        task_id='end',
        dag=dag
    )

    # Create group1
    with TaskGroup("TaskGroup_1", tooltip="Tasks for taskgroup_1") as taskgroup_1:
        task_a = BashOperator(task_id="task_A", bash_command='echo 1')
        task_b = DummyOperator(task_id="task_B")
        task_c = DummyOperator(task_id="task_C")

        # Define dependencies for group1
        # Execute a after that execute q and r SEQUENCIALLY
        task_a >> task_b >> task_c

    # Create group1
    with TaskGroup("TaskGroup_2", tooltip="Tasks for taskgroup_2") as taskgroup_2:
        task_p = BashOperator(task_id="task_P", bash_command='echo 1')
        task_q = DummyOperator(task_id="task_Q")
        task_r = DummyOperator(task_id="task_R")

        # Define dependencies for group2
        # Execute p after that execute q and r PARALLELLY
        task_p >> [task_q, task_r]


# Define dependencies

start >> taskgroup_1 >> taskgroup_2 >> end
