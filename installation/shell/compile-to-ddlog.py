#!/usr/bin/env python3

## Compiles a splog.json file (output by spannerlog.jar) to a app.ddlog file.


import os
import json
import sys
from collections import OrderedDict


def main():
    with open(sys.argv[1]) as conf_file:
        conf = json.load(conf_file, object_pairs_hook=OrderedDict)

        compile_db_schema(conf["schema"])       
        # compile_ie_functions(conf["ie_functions"], conf["schema"], sys.argv[2])
        compile_rules(conf["schema"]["idb"], conf["execution"]["idb"])


def compile_db_schema(schema):
    if "edb" in schema:
        compile_sub_schema(schema["edb"])

    if "idb" in schema:
        compile_sub_schema(schema["idb"])

    # if "ief" in schema:
    #   compile_sub_schema(schema["ief"])


def get_attribute_list(schema):
    attrs = []
    for attr_name, attr_type in schema["attributes"].items():
        if attr_type == "span":
            attrs.append((attr_name+"_start", "int"))
            attrs.append((attr_name+"_end", "int"))
        else:
            attrs.append((attr_name, attr_type))
    return attrs


def compile_sub_schema(sub_schame):
    for rel_schema in sub_schame:
        predVar = "?" if "variable_type" in rel_schema else ""
        print(rel_schema["name"] + predVar + " (")
        attrs = get_attribute_list(rel_schema)

        attr_strings = ['{0:<18} {1:<}'.format(attr_name, attr_type) for attr_name, attr_type in attrs]
        print("\t" + ",\n\t".join(attr_strings) + "\n).\n")


def compile_ie_functions(ie_functions, schema, target_udf_dir):
    pass # TODO implement
    # for ief in ie_functions:
    #   name = ief["name"]

    #   print("function " + name + " over (s text)\n\t" + \
    #         "returns rows like " + name + "\n\t" + \
    #         "implementation \"udf/" + name + ".py\" handles tsv lines.\n\n" + \
    #         ief["statement"] + "\n")

    #   if "regex" in ief:
    #       create_regex_udf(ief, 
    #           [rel_schema["attributes"] for rel_schema in schema if rel_schema["name"] == name][0],
    #           target_udf_dir)


def create_regex_udf(ief, attrs, target_udf_dir):
    with open(os.path.join(target_udf_dir, ief["name"]+".py"), "w") as outfile:
        outfile.write("#!/usr/bin/env python\n\n")
        outfile.write("from deepdive import *\n\n")
        outfile.write("import re\n\n")
        outfile.write("@tsv_extractor\n")
        outfile.write("@returns(lambda\n")
        for attr_name, attr_type in attrs.items():
            if attr_type != "span":
                outfile.write("\t%s = \"%s\",\n" % (attr_name, attr_type))
            else:
                outfile.write("\t%s_start = \"int\",\n" % (attr_name, ))
                outfile.write("\t%s_end = \"int\",\n" % (attr_name, ))
        outfile.write(":[])\n")
        outfile.write("def %s(s = \"text\"):\n\n" % (ief["name"], ))
        outfile.write("\tpattern = re.compile(r\"%s\")\n" % (ief['regex'], ))
        outfile.write("\tmatch = pattern.match(s)\n")
        outfile.write("\tif match:\n")
        outfile.write("\t\tyield [\n")
        outfile.write("\t\t\ts,\n")
        for attr in list(attrs.keys())[1:]:
            outfile.write("\t\t\tmatch.start('%s') + 1,\n" % (attr, ))
            outfile.write("\t\t\tmatch.end('%s') + 1,\n" % (attr, ))
        outfile.write("\t\t]\n\n")
        # outfile.write("\telse:\n")
        # outfile.write("\t\tyield [\"ds\",1,2,3,4]\n\n")


def compile_rules(isch, rules):

    # Printing each ddlog-compiled rule
    printed = []
    for name, rule in rules.items():
        if rule["target"] == "ddlog":
            print(rule["cmd"])
            printed.append(name)

    # Creating a dummy rule for each i-schema without a ddlog-compiled rule.
    for sch in isch:
        if sch["name"] not in printed:
            # attrs = [ "v" + str(i) for i in range(len(get_attribute_list(sch)))]
            # atom_str = sch["name"] + "(" + ", ".join(attrs) + ")"
            # print(atom_str + " :- " + atom_str + ", 0 > 1.")

            attrs = []
            for attr_name, attr_type in get_attribute_list(sch):
                if attr_type == "int":
                    attrs.append("0")
                elif attr_type == "text":
                    attrs.append("\"\"")
                elif attr_type == "span":
                    attrs.append("0")
                    attrs.append("1")
            atom_str = sch["name"] + "(" + ", ".join(attrs) + ")"
            print(atom_str + " :- anchor(_), [0 > 1].")
            # print(atom_str + " :- 0 > 1.")
            # print(atom_str + " :- articles(x,y).")


if __name__ == "__main__":
    main()
