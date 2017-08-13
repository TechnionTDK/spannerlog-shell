#!/usr/bin/env python

## Compiles a splog.json file (output by spannerlog.jar) to psql code for regex formulas.


import os
import json
import sys
from collections import OrderedDict


def main():
	with open(sys.argv[1]) as conf_file:
		conf = json.load(conf_file, object_pairs_hook=OrderedDict)
	
		compile_ief(conf["ief"]["rgx"], conf["schema"]["ief"])


def compile_ief(regex_formulas, schema):
	for rgx in regex_formulas:
		attrs = [rgx_sch["attributes"] for rgx_sch in schema if rgx_sch["name"] == rgx["name"]][0]
		create_regex_udf(rgx, attrs)
		

def create_regex_udf(ief, attrs):
	table_cols = [];
	for attr_name, attr_type in attrs.items()[1:]:
		if attr_type != "span":
			table_cols.append("%s %s" % (attr_name, attr_type))
		else:
			table_cols.append("%s_start int" % (attr_name, ))
			table_cols.append("%s_end int" % (attr_name, ))
	print("CREATE FUNCTION %s(s text)" % (ief["name"], ))
	print("\tRETURNS TABLE (%s)" % (", ".join(table_cols), ))
	print("AS $$\n")
	print("import re\n")
	print("pattern = re.compile(r\"%s\")" % (ief['regex'], ))
	print("match = pattern.match(s)")
	print("if match:")
	print("\tyield [")
	for attr in list(attrs.keys())[1:]:
		print("\t\tmatch.start('%s') + 1," % (attr, ))
		print("\t\tmatch.end('%s') + 1," % (attr, ))
	print("\t]\n")
	print("$$ LANGUAGE plpythonu;")
	# print("\telse:\n")
	# print("\t\tyield [\"ds\",1,2,3,4]\n\n")


if __name__ == "__main__":
	main()
