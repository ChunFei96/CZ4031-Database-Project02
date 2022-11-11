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
