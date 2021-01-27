
from airflow import DAG
from airflow.exceptions import AirflowSkipException
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow'
}

# Create some placeholder operators
class DummySkipOperator(DummyOperator):

    """Dummy operator which always skips the task."""

    ui_color = '#e8b7e4'

    def execute(self, context):
        raise AirflowSkipException

def create_test_pipeline(suffix, trigger_rule, dag_):

    """
    Instantiate a number of operators for the given DAG.

    :param str suffix: Suffix to append to the operator task_ids
    :param str trigger_rule: TriggerRule for the join task
    :param DAG dag_: The DAG to run the operators on
    """
    skip_operator = DummySkipOperator(task_id=f'skip_operator_{suffix}', dag=dag_)
    always_true = DummyOperator(task_id=f'always_true_{suffix}', dag=dag_)
    join = DummyOperator(task_id=trigger_rule, dag=dag_, trigger_rule=trigger_rule)
    final = DummyOperator(task_id=f'final_{suffix}', dag=dag_)

    skip_operator >> join
    always_true >> join
    join >> final


dag = DAG(dag_id='tms_practice_skip_dag', default_args=args, start_date=days_ago(2), tags=['example'])
create_test_pipeline('1', 'all_success', dag)
create_test_pipeline('2', 'one_success', dag)
