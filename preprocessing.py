import csv
import os
import psycopg2
import json
from tkinter import messagebox


# PREPROCESSING .TBL FILES TO CSV
def tbl_to_csv(filename):
    csv = open("".join([filename, ".csv"]), "w+")

    tbl = open("".join([filename, ".tbl"]), "r")
    lines = tbl.readlines()
    for line in lines:
        length = len(line)
        line = line[:length - 2] + line[length-1:]
        csv.write(line)
    tbl.close()
    csv.close()


# GET JSON
# [
#   {
#       key: '123',
#       value: 0 or 1 // 0 for disable, 1 for enable
#   }
# ]
def get_json(inputValue, enableList):
    """ read json content """
    with open("config.json", 'r') as f:
        config = json.loads(f.read())
        print(config)

    """" preprocssing with checkbox array """
    _list = []
    for v in enableList:
        _list.append("SET LOCAL {} = {};\n".format(
            v['key'], "OFF" if int(v['value']) == 0 else "ON"))
    params_enable = ''.join(_list)

    """ query parts from the parts table """
    conn = None
    x = None

    try:
        # connect to postgres in this format
        conn = psycopg2.connect(config['pg_db'])
        cur = conn.cursor()

        cur.execute(params_enable +
                    "EXPLAIN (ANALYZE, VERBOSE, FORMAT JSON)" + inputValue)
        rows = cur.fetchall()
        x = json.dumps(rows)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        messagebox.showerror("Error", error)
        print(error)
    finally:
        if conn is not None:
            conn.close()
    print("success")
    return x


# DATABASE CONNECTION
def connect():
    """ read json content """
    with open("config.json", 'r') as f:
        config = json.loads(f.read())
        print(config)

    conn = None
    x = None
    try:
        params = config["pg_db"]

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Data`base connection closed.')
    cur = conn.cursor()


connect()

# Main
filenames = [
    "customer",
    "lineitem",
    "nation",
    "orders",
    "part",
    "partsupp",
    "region",
    "supplier",
]

for filename in filenames:
    tbl_to_csv(filename)
