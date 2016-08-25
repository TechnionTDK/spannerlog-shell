#!/usr/bin/env python3
import os
import json
import inspect
from importlib.machinery import SourceFileLoader
import sys


DIR_SRC_NAME = 'udf'
DIR_DST_NAME = os.path.join('target', 'udf')


def main():
	global DIR_SRC_NAME, DIR_DST_NAME

	# create directory for compiled UDFs
	os.mkdir(DIR_DST_NAME)

	db_schema = {}	

	# iterate over all python files in 'udf' directory
	for filename in os.listdir(DIR_SRC_NAME):
		if filename.endswith('.py'):

			# load module
			module_name = os.path.splitext(filename)[0]
			module = SourceFileLoader(module_name, os.path.join(DIR_SRC_NAME, filename)).load_module()
			
			udf_schema = extract_udf_schema(module)
			create_deepdive_udf(module, udf_schema, filename, module_name)

			db_schema[module_name] = udf_schema

	print(json.dumps(db_schema, sort_keys=True, indent=4))


def create_deepdive_udf(module, udf_schema, filename, module_name):
	global DIR_DST_NAME

	with open(os.path.join(DIR_DST_NAME, filename), "w") as outfile:
		functions = inspect.getmembers(module, predicate=inspect.isfunction)
		f_list = [func for name, func in functions if name == module_name]
		if not f_list:
			exit_with_message("IE function is missing: expecting a function with the name of the file")
		if len(inspect.signature(f_list[0]).parameters) != 1:
			exit_with_message("IE function should have a single parameter")

		for line in inspect.getsourcelines(module)[0]:
			if "def %s" % (module_name,) in line:
				outfile.write("\nfrom deepdive import *\n\n\n")
				outfile.write("@tsv_extractor\n")
				outfile.write("@returns(lambda\n")
				for col_name, col_type in udf_schema.items():
					if col_type != "span":
						outfile.write("\t%s = \"%s\",\n" % (col_name, col_type))
					else:
						outfile.write("\t%s_start = \"int\",\n" % (col_name, ))
						outfile.write("\t%s_end = \"int\",\n" % (col_name, ))
				outfile.write(":[])\n")
				outfile.write(line)
			else:
				outfile.write(line)


def exit_with_message(msg):
	red = '\033[91m'
	native = '\033[m'
	sys.stderr.write(red+msg+'\n'+native)
	sys.exit()


def extract_udf_schema(module):
	udf_schema = {}
	comments = [c[2:].split() for c in inspect.getcomments(module).split('\n') if c.startswith("#.")]
	return {col_name: col_type for col_name, col_type in comments}


if __name__ == "__main__":
    main()
