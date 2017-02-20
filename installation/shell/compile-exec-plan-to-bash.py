#!/usr/bin/env python3

## Compiles the execution plan specified in splod.json into a bash script

import os
import json
import sys
from collections import OrderedDict
import re

def main():
    print("#!/usr/bin/env bash\n")

    with open(sys.argv[1]) as conf_file:
        conf = json.load(conf_file, object_pairs_hook=OrderedDict)

        # for name in conf["execution"]["edb"]:
        #     print("deepdive do process/init/relation/" + name + " > /dev/null")
        #     print("deepdive do data/" + name + " > /dev/null")

        print("deepdive do all > /dev/null")

        for name, steps in conf["execution"]["idb"].items():
            sql_steps = []
            ddlog_steps_exist = None
            for step in steps:
                if step["target"] == "sql":
                    sql_steps.append(re.sub(r"\"(.*?)\"", r"'\1'::text", step["cmd"]))
                if step["target"] == "ddlog":
                    ddlog_steps_exist = True

            if ddlog_steps_exist:
                print("deepdive redo process/ext_" + name + " > /dev/null")
                print("deepdive redo data/" + name + " > /dev/null")
                print()
                # print("deepdive do " + name + " > /dev/null")
                if sql_steps:
                    print("deepdive sql \"INSERT INTO " + name + " " + "\nUNION ALL\n".join(sql_steps) + "\"\n")
            elif sql_steps:
                print("deepdive db create-table-as " + name + " \"" + "\nUNION ALL\n".join(sql_steps) + "\"\n")


if __name__ == "__main__":
    main()
