#!/usr/bin/env python

from deepdive import *  # Required for @tsv_extractor and @returns

import re

@tsv_extractor  # Declares the generator below as the main function to call
@returns(lambda 
        s = "text",
        x = "text",
    :[]) # Declares the types of output columns as declared in DDlog
def rgx2(   # The input types can be declared directly on each parameter as its default value
        s = "text"
    ):
	
	# yield [s, "1,5"]
	pattern = r"(?P<x>[b]+)"
	regex = re.compile(pattern)
	for match in regex.finditer(s):
		yield [ s, str(match.start('x') + 1) + "," + str(match.end('x') + 1) ]
