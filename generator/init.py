import os
from utils.connector import Connector
from generators.spellers import Spellers
from generators.spells import Spells
import time

def init_schema(conn):
    init_scripts = list()
    for schema in os.listdir('schema'):
        with open(os.path.join('schema', schema)) as sch_file:
            init_scripts.append(sch_file.read())

    conn.execute_batch(init_scripts)

def single_step(spellers, spells):
    spellers.insert(20)
    spells.insert(40)


if __name__ == "__main__":
    time.sleep(20)
    conn = Connector('prod_db')
    spellers = Spellers(conn)
    spells = Spells(conn, spellers)

    init_schema(conn)
    
    while True:
        print("Next step")
        single_step(spellers, spells)
        time.sleep(10)

