import time
import psycopg2
import os

#DB-API
stage_connector = psycopg2.connect(
    user='pguser',
    password='pgpassword',
    database='magic',
    host='stage_db'
)

prod_connector = psycopg2.connect(
    user='pguser',
    password='pgpassword',
    database='magic',
    host='prod_db'
)

def init_stage_tables():
    with stage_connector.cursor() as cursor:
        for schema in os.listdir('schemas'):
            with open(os.path.join('schemas', schema)) as f:
                cursor.execute(f.read())
        stage_connector.commit()
    print("schema inited")

def get_data(tname):
    with prod_connector.cursor() as cursor:
        fpath = os.path.join("/dumps","{}.csv".format(tname))
        try:
            os.remove(fpath)
        except:
            pass
        with open(fpath, "w+") as ifile:
            cursor.copy_expert('''COPY (SELECT * FROM {}) TO STDOUT WITH (FORMAT CSV)'''.format(tname), ifile)
    print("dumped", tname)

def put_data(tname):
    with stage_connector.cursor() as cursor:
        fpath = os.path.join("/dumps","{}.csv".format(tname))
        with open(fpath) as ofile:
            cursor.copy_expert('''COPY {} FROM STDIN WITH (FORMAT CSV)'''.format(tname), ofile)
        stage_connector.commit()
    print("uploaded", tname)

if __name__ == "__main__":
    init_stage_tables()
    for tname in ["spellers", "spells"]:
        get_data(tname)
        put_data(tname)
    while True:
        time.sleep(20)
