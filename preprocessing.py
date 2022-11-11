import csv
import os
import psycopg2
import json
from tkinter import messagebox


class Preprocessing:

    def get_json(inputValue, enableList):
        """ read json content """
        with open("config.json", 'r') as f:
            config = json.loads(f.read())
            print(config)

        """" preprocssing with checkbox array """
        _list = []
        for key in enableList:
            _list.append("SET LOCAL {} = {};\n".format(
                key, "OFF" if int(enableList[key]) == 0 else "ON"))
        params_enable = ''.join(_list)

        """ query parts from the parts table """
        conn = None
        json_QEP = None
        json_AQP = None

        try:
            # connect to postgres in this format
            db_conf = config['pg_db']
            conn = psycopg2.connect(
                host=db_conf["host"],
                database=db_conf["database"],
                user=db_conf["user"],
                password=db_conf["password"],
                port=db_conf["port"]
            )
            cur = conn.cursor()

            # execute query to retrieve QEP is json
            cur.execute("EXPLAIN (ANALYZE, VERBOSE, FORMAT JSON)" + inputValue)
            rows = cur.fetchall()
            json_QEP = json.dumps(rows)

            # execute query to retrieve AQP in json
            cur.execute(params_enable +
                        "EXPLAIN (ANALYZE, VERBOSE, FORMAT JSON)" + inputValue)
            rows = cur.fetchall()
            json_AQP = json.dumps(rows)

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            messagebox.showerror("Error", error)
            print(error)
        finally:
            if conn is not None:
                conn.close()
        print("success")
        return json_QEP, json_AQP

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

    # for filename in filenames:
    #    tbl_to_csv(filename)
