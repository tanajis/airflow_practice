from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.subdag import SubDagOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

def create_subdag(parent_dag_id):
    # Create Subdag(inner dag)
    with DAG(
            dag_id="{}.subdag1".format(parent_dag_id)
            , default_args=args
            , start_date=days_ago(2)
            , schedule_interval="@once"
            , tags=['tms_practice']) as subdag:
        start = DummyOperator(task_id="start", dag=subdag)
        end = DummyOperator(task_id="end", dag=subdag)
        start >> end

        return subdag

with DAG(
     dag_id="tms_practice_subdag_operator"
    , default_args=args
    , start_date=days_ago(2)
    , schedule_interval="@once"
    , tags=['tms_practice']) as outer_dag:

    start = DummyOperator(
        task_id='start',
        dag=outer_dag,
    )

    end = DummyOperator(
        task_id='end',
        dag=outer_dag,
    )


    # Create subdag Operator
    subdag1 = SubDagOperator(
        task_id='subdag1',
        subdag=create_subdag("tms_practice_subdag_operator"),
        dag=outer_dag
    )

    # Define Dependencies
    start >> subdag1 >> end