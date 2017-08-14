#!/usr/bin/env python3

## Compiles a splog.json file (output by spannerlog.jar) to a app.ddlog file.


import os
import json
import sys
from collections import OrderedDict


class DdlogCompiler(object):

    def __init__(self):
        self.schema = []
        self.rules = []


    def compile_db_schema(self, schema_dict):
        if "edb" in schema_dict:
            self.compile_sub_schema(schema_dict["edb"])

        if "idb" in schema_dict:
            self.compile_sub_schema(schema_dict["idb"])

        # if "ief" in schema_dict:
        #   self.compile_sub_schema(schema_dict["ief"])


    def get_attribute_list(self, schema):
        attrs = []
        for attr_name, attr_type in schema["attributes"].items():
            if attr_type == "span":
                attrs.append((attr_name+"_start", "int"))
                attrs.append((attr_name+"_end", "int"))
            else:
                attrs.append((attr_name, attr_type))
        return attrs


    def compile_sub_schema(self, sub_schame):
        for rel_schema in sub_schame:
            predVar = "?" if "variable_type" in rel_schema else ""
            schema_str = rel_schema["name"] + predVar + " (\n"
            attrs = self.get_attribute_list(rel_schema)

            attr_strings = ['{0:<18} {1:<}'.format(attr_name, attr_type) for attr_name, attr_type in attrs]
            schema_str = schema_str + "\t" + ",\n\t".join(attr_strings) + "\n).\n"

            self.schema.append(schema_str)


    def compile_ie_functions(self, ie_functions, schema, target_udf_dir):
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


    def create_regex_udf(self, ief, attrs, target_udf_dir):
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


    def compile_rules(self, isch, rules):

        # Printing each ddlog-compiled rule
        printed = []
        for name, steps in rules.items():
            for step in steps:
                if step["target"] == "ddlog":
                    self.rules.append(step["cmd"] + "\n")
                    printed.append(name)            

        using_dummy = False           
        # Creating a dummy rule for each i-schema without a ddlog-compiled rule.
        for sch in isch:
            if sch["name"] not in printed:
                # attrs = [ "v" + str(i) for i in range(len(self.get_attribute_list(sch)))]
                # atom_str = sch["name"] + "(" + ", ".join(attrs) + ")"
                # print(atom_str + " :- " + atom_str + ", 0 > 1.")

                attrs = []
                for attr_name, attr_type in self.get_attribute_list(sch):
                    if attr_type == "int":
                        attrs.append("0")
                    elif attr_type == "text":
                        attrs.append("\"\"")
                    elif attr_type == "span":
                        attrs.append("0")
                        attrs.append("1")
                atom_str = sch["name"] + "(" + ", ".join(attrs) + ")"
                self.rules.append(atom_str + " :- dummy(_), [0 > 1].\n")
                using_dummy = True
                # print(atom_str + " :- 0 > 1.")
                # print(atom_str + " :- articles(x,y).")

        if using_dummy:
            schema_str = "dummy(\n\t" + '{0:<18} {1:<}'.format("attr", "int") + "\n).\n"
            self.schema.append(schema_str)

    def print(self):
        print(self.schema.join("\n"))
        print("\n")
        print(self.rules.join("\n"))


def main():
    with open(sys.argv[1]) as conf_file:
        conf = json.load(conf_file, object_pairs_hook=OrderedDict)

        compiler = DdlogCompiler()

        compiler.compile_db_schema(conf["schema"])       
        # compile_ie_functions(conf["ie_functions"], conf["schema"], sys.argv[2])
        compiler.compile_rules(conf["schema"]["idb"], conf["execution"]["idb"])

        compiler.print()


if __name__ == "__main__":
    main()
