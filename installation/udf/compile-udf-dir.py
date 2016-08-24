#!/usr/bin/env python3
import os
import json
import inspect
from importlib.machinery import SourceFileLoader


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
		outfile.write(inspect.getsource(module))
		outfile.write("\n\n\nfrom deepdive import *\n\n\n")
		outfile.write("@tsv_extractor\n")
		outfile.write("@returns(lambda\n")
		for col_name, col_type in udf_schema.items():
			if col_type != "span":
				outfile.write("\t%s = \"%s\",\n" % (col_name, col_type))
			else:
				outfile.write("\t%s_start = \"int\",\n" % (col_name, ))
				outfile.write("\t%s_end = \"int\",\n" % (col_name, ))
		outfile.write(":[])\n")
		outfile.write("def %s(s = \"text\"):\n" % (module_name,))
		# print(inspect.getsourcelines(module.iefunc))
		for line in inspect.getsourcelines(module.iefunc)[0][1:]:
			outfile.write(line)



def extract_udf_schema(module):
	udf_schema = {}
	comments = [c[2:].split() for c in inspect.getcomments(module).split('\n') if c.startswith("#.")]
	return {col_name: col_type for col_name, col_type in comments}


if __name__ == "__main__":
    main()
