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

def get_data(tname, start_row = 0):
    with prod_connector.cursor() as cursor:
        fpath = os.path.join("/dumps","{}.csv".format(tname))
        try:
            os.remove(fpath)
        except:
            pass
        with open(fpath, "w+") as ifile:
            cursor.copy_expert('''COPY (SELECT * FROM {} WHERE {} > {}) TO STDOUT WITH (FORMAT CSV)'''
            .format(tname,tname[:-1]+'_id',start_row), ifile)
    print("dumped", tname)

def put_data(tname):
    with stage_connector.cursor() as cursor:
        fpath = os.path.join("/dumps","{}.csv".format(tname))
        with open(fpath) as ofile:
            cursor.copy_expert('''COPY {} FROM STDIN WITH (FORMAT CSV)'''.format(tname), ofile)
        stage_connector.commit()
    print("uploaded", tname)

def get_maxID(tname):
    with stage_connector.cursor() as cursor:
        cursor.execute("SELECT max({}) from {}".format(tname[:-1]+'_id',tname))
        record = cursor.fetchall()
    print("Результат", record[0][0])
    return record[0][0]

if __name__ == "__main__":
    while True:
        try:
            init_stage_tables()
            break
        except:
            time.sleep(15)
    
    #for tname in ["spellers", "spells"]:
    #    get_data(tname,get_maxID(tname))
    #    put_data(tname)
    while True:
        time.sleep(20)
