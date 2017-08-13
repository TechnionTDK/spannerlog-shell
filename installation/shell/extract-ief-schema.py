#!/usr/bin/env python3
import os
import json
import inspect
from importlib.machinery import SourceFileLoader
import sys
from collections import OrderedDict


DIR_SRC_NAME = sys.argv[1]


def main():
	global DIR_SRC_NAME

	db_schema = {}	

	# iterate over all python files in 'ief' directory
	for filename in os.listdir(DIR_SRC_NAME):
		if filename.endswith('.py'):

			# load module
			module_name = os.path.splitext(filename)[0]
			module = SourceFileLoader(module_name, os.path.join(DIR_SRC_NAME, filename)).load_module()

			db_schema[module_name] = extract_ief_schema(module)

	print(json.dumps(db_schema, sort_keys=False, indent=4))


def exit_with_message(msg):
	red = '\033[91m'
	native = '\033[m'
	sys.stderr.write(red+msg+'\n'+native)
	sys.exit()


def extract_ief_schema(module):
	comments = [c[2:].split() for c in inspect.getcomments(module).split('\n') if c.startswith("#.")]
	return OrderedDict([(col_name, col_type) for col_name, col_type in comments])


if __name__ == "__main__":
    main()
