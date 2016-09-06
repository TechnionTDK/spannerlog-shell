#!/usr/bin/env python

#. content_in		text
#. content_out	 	text 

import re

from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')

def preprocess(s):

	t = str(s.decode('ascii', 'ignore'))
	t = t.replace('\n', ' ').replace('\r', ' ').replace('\\n', ' ')
	t = t.strip()
	t = re.sub('\s+', ' ', t)


	yield [s, t]
