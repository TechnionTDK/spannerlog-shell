#!/usr/bin/env python3
import csv
import os
import json
import sys
import subprocess

from collections import OrderedDict


def main():

    db_schema = {}

    for filename in os.listdir(sys.argv[1]):
        if filename.endswith('.tsv') or filename.endswith('.csv'):
            delim = "\t" if filename.endswith('.tsv') else ","
            filepath = os.path.join(sys.argv[1], filename)
            with open(filepath, encoding="utf-8", errors = 'ignore') as infile:
                reader = csv.reader(infile, delimiter=delim)
                
                table_name = os.path.splitext(filename)[0]
                headers = reader.next()
                record = reader.next()
                print(headers)
                print(record)
                db_schema[table_name] = extract_table_schema(headers, record)

            cmd = "tail -n +2 %s > %s.temp; mv %s.temp %s" % (filepath, filepath, filepath, filepath)
            df = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = df.communicate()


    print(json.dumps(db_schema, sort_keys=True, indent=4))


def extract_table_schema(headers, record):
    cnt = 1
    table_schema = OrderedDict()

    for i, val in enumerate(record):
        if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
            attr_type = 'int'
        elif val.replace('.','',1).isdigit() or (val.startswith('-') and val[1:].replace('.','',1).isdigit()):
            attr_type = 'float'
        else:
            attr_type = "text"

        # table_schema["column" + str(cnt)] = attr_type
        table_schema[headers[i]] = attr_type
        cnt += 1

    return table_schema


if __name__ == "__main__":
    main()
