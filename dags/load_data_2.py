from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook

import datetime

def get_maxID(tname):
    ph = PostgresHook(postgres_conn_id = "stage")
    stage_connector = ph.get_conn()
    with stage_connector.cursor() as cursor:
        cursor.execute("SELECT max({}) from {}".format(tname[:-1]+'_id',tname))
        record = cursor.fetchall()
    print("Max row", record[0][0])
    return record[0][0]

def dump_data(tname):
    start_row = get_maxID(tname)
    if not start_row:
        start_row = 0
    ph = PostgresHook(postgres_conn_id = "prod")
    prod_connector = ph.get_conn()
    with prod_connector.cursor() as cursor:
        with open(tname + ".csv", "w") as ifile:
            cursor.copy_expert('''COPY (SELECT * FROM {} where {} > {}) TO STDOUT WITH (FORMAT CSV)'''
            .format(tname, tname[:-1]+'_id', start_row), ifile)
    return

def load_data(tname):
    ph = PostgresHook(postgres_conn_id = "stage")
    stage_connector = ph.get_conn()
    with stage_connector.cursor() as cursor:
        with open(tname + ".csv") as ofile:
            cursor.copy_expert('''COPY {} FROM STDIN WITH (FORMAT CSV)'''.format(tname), ofile)
    stage_connector.commit()
    return

with DAG(
    dag_id="data_dumper_2",
    start_date=datetime.datetime(2021,11,25),
    schedule_interval="@once",
    catchup=False
) as dag:

    dump_from_prod_spells = PythonOperator(
        task_id = "dump_data",
        python_callable = dump_data,
        op_kwargs = {
            'tname': 'spells',
            }
    )

    load_to_stage_spells = PythonOperator(
        task_id = "load_data",
        python_callable = load_data,
        op_kwargs = {
            'tname': 'spells',
            }
    )

    dump_from_prod_spellers = PythonOperator(
        task_id = "dump_data2",
        python_callable = dump_data,
        op_kwargs = {
            'tname': 'spellers',
            }
    )

    load_to_stage_spellers = PythonOperator(
        task_id = "load_data2",
        python_callable = load_data,
        op_kwargs = {
            'tname': 'spellers',
            }
    )

    dump_from_prod_spells >> load_to_stage_spells 
    dump_from_prod_spellers >> load_to_stage_spellers
