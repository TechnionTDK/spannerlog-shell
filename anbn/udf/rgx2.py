#!/usr/bin/env python

#. s 	text
#. x	span


import re


def rgx2(s):
	
	# yield [s, "1,5"]
	pattern = r"(?P<x>[b]+)"
	regex = re.compile(pattern)
	for match in regex.finditer(s):
		yield [ s, str(match.start('x') + 1) + "," + str(match.end('x') + 1) ]
