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

def dump_data():
    start_row = get_maxID('spells')
    if not start_row:
        start_row = 0
    ph = PostgresHook(postgres_conn_id = "prod")
    prod_connector = ph.get_conn()
    with prod_connector.cursor() as cursor:
        with open("spells.csv", "w") as ifile:
            cursor.copy_expert('''COPY (SELECT * FROM spells where spell_id > {}) TO STDOUT WITH (FORMAT CSV)'''.format(start_row), ifile)
    return

def load_data():
    ph = PostgresHook(postgres_conn_id = "stage")
    stage_connector = ph.get_conn()
    with stage_connector.cursor() as cursor:
        with open("spells.csv") as ofile:
            cursor.copy_expert('''COPY spells FROM STDIN WITH (FORMAT CSV)''', ofile)
    stage_connector.commit()
    return

with DAG(
    dag_id="data_dumper",
    start_date=datetime.datetime(2021,11,25),
    schedule_interval="@once",
    catchup=False
) as dag:

    clear_data_stage = PostgresOperator(
        postgres_conn_id = "stage",
        task_id = "truncate_spells",
        sql = """TRUNCATE spells"""
    )

    dump_from_prod = PythonOperator(
        task_id = "dump_data",
        python_callable = dump_data
    )

    load_to_stage = PythonOperator(
        task_id = "load_data",
        python_callable = load_data
    )

    clear_data_stage >> dump_from_prod >> load_to_stage
