#!/usr/bin/env python

#. s 	text
#. x	span
#. y 	span 


import re


def rgx1(s):

	# yield [s, 1, 5, 5, 9]

	pattern = r"^(?P<x>[a]+)(?P<y>[b]+$)"
	regex = re.compile(pattern)
	for match in regex.finditer(s):
		yield [
		    s, 
		    match.start('x') + 1, 
		    match.end('x') + 1, 
		    match.start('y') + 1,
		    match.end('y') + 1
		]
