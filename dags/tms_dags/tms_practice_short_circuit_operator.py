
from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import ShortCircuitOperator
from airflow.utils import dates

args = {
    'owner': 'airflow'
}


dag = DAG(
    dag_id='tms_practice_short_circuit_operator',
    default_args=args,
    start_date=dates.days_ago(2),
    tags=['tms_practice'],
)

# below will return always true
cond_true = ShortCircuitOperator(
    task_id='condition_is_True',
    python_callable=lambda: True,
    dag=dag,
)

# Below will return always false
cond_false = ShortCircuitOperator(
    task_id='condition_is_False',
    python_callable=lambda: False,
    dag=dag,
)
# Create Dummy Operators
ds_true = [DummyOperator(task_id='true_' + str(i), dag=dag) for i in [1, 2]]
ds_false = [DummyOperator(task_id='false_' + str(i), dag=dag) for i in [1, 2]]

# Create chain Operator of these tasks
chain(cond_true, *ds_true)
chain(cond_false, *ds_false)