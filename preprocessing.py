import csv
import os


# PREPROCESSING .TBL FILES TO CSV
def tbl_to_csv(filename):
    csv = open("".join([filename, ".csv"]), "w+")

    tbl = open("".join([filename, ".tbl"]), "r")
    lines = tbl.readlines()
    for line in lines:
        length = len(line)
        line = line[:length - 2] + line[length-1:]
        line = line.replace(",", "N")
        line = line.replace("|", ",")
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

for filename in filenames:
    tbl_to_csv(filename)
