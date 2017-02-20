#!/usr/bin/env python3

## Compiles the execution plan specified in splod.json into a bash script

import os
import json
import sys
from collections import OrderedDict


def main():
    print("#!/usr/bin/env bash\n")

    with open(sys.argv[1]) as conf_file:
        conf = json.load(conf_file, object_pairs_hook=OrderedDict)

        # for name in conf["execution"]["edb"]:
        #     print("deepdive do process/init/relation/" + name + " > /dev/null")
        #     print("deepdive do data/" + name + " > /dev/null")

        print("deepdive do all > /dev/null")

        for name, rule in conf["execution"]["idb"].items():
            if rule["target"] == "sql":
                print("deepdive db create-table-as " + name + " \"" + rule["cmd"] + "\"")
            elif rule["target"] == "ddlog":
                print("deepdive redo process/ext_" + name + " > /dev/null")
                print("deepdive redo data/" + name + " > /dev/null")
                # print("deepdive do " + name + " > /dev/null")


if __name__ == "__main__":
    main()
