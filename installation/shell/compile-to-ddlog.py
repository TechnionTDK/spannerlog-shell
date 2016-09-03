#!/usr/bin/env python3

import json
import sys
from collections import OrderedDict

def main():

	with open(sys.argv[1]) as conf_file:
		conf = json.load(conf_file, object_pairs_hook=OrderedDict)

		compile_schema(conf["schema"])
		compile_ie_functions(conf["ie-functions"])
		compile_rules(conf["rules"])


def compile_schema(schema):
	for rel_schema in schema:
		print(rel_schema["name"] + " (")
		attrs = []
		for attr_name, attr_type in rel_schema["attributes"].items():
			if attr_type == "span":
				attrs.append((attr_name+"_start", "int"))
				attrs.append((attr_name+"_end", "int"))
			else:
				attrs.append((attr_name, attr_type))

		attr_strings = ['{0:<12} {1:<}'.format(attr_name, attr_type) for attr_name, attr_type in attrs]
		print("\t" + ",\n\t".join(attr_strings) + "\n).\n")


def compile_ie_functions(ie_functions):
	for ief in ie_functions:
		name = ief["name"]

		print("function " + name + " over (s text)\n\t" + \
			  "returns rows like " + name + "\n\t" + \
			  "implementation \"udf/" + name + ".py\" handles tsv lines.\n\n" + \
			  ief["function-call-rule"] + "\n")


def compile_rules(rules):
	for rule in rules:
		print(rule + "\n")


if __name__ == "__main__":
	main()
