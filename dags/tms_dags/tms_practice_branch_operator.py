from select import select

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator,BranchPythonOperator
from airflow.utils.dates import days_ago
from datetime import date
args = {
    'owner': 'airflow'
}


def process_week_start():
    print('***Processing Week Start***')
    return True


def process_week_end():
    print('***Processing Week end***')
    return True


def process_week_days():
    print('***Processing Week days***')
    return True


def select_from_branch():
    """
    Returns task id based on condition.
    :return: task_id
    """

    current_date = date.today()
    if current_date.strftime('%A') == 'Monday':
        return "week_start_task"

    elif current_date.strftime('%A') == 'Friday':
        return "week_end_task"
    else:
        return "week_days_task"


dag = DAG(
    dag_id='tms_practice_branch_operator',
    default_args=args,
    start_date=days_ago(3),
    schedule_interval=None,
    tags=['tms-practice'],)

start = DummyOperator(
    task_id='start',
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)

week_start_task = PythonOperator(
    task_id='week_start_task',
    python_callable=process_week_start,)

week_end_task = PythonOperator(
    task_id='week_end_task',
    python_callable=process_week_end,)

week_days_task = PythonOperator(
    task_id='week_days_task',
    python_callable=process_week_days
)

branch = BranchPythonOperator(
    task_id="Branch",
    dag=dag,
    python_callable=select_from_branch
)


join = DummyOperator(
    task_id='join',
    trigger_rule='none_failed_or_skipped',
    dag=dag,
)

# Define dependencies

start >> branch

branch >> week_days_task >> join
branch >> week_end_task >> join
join >> end

"""
Note :
Above dependencies can also be defined in single line as  below
start >> branch >> [week_start_task,week_days_task,week_end_task] >> join >>end
"""
