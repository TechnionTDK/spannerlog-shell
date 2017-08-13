#!/usr/bin/env python

import pprint as pp
from pycorenlp import StanfordCoreNLP
import re


nlp = StanfordCoreNLP('http://localhost:9000')


def main():
	

	s = "Barack Obama married Michelle Obama in 1969"
	
	for res in rgx(s):
		pp.pprint(res)

	# for res in ner(s):
	# 	pp.pprint(res)

def rgx(s):
	pattern = re.compile(r"(?P<x>[A-Z][a-z]*( [A-Z][a-z]*)*) married (?P<y>[A-Z][a-z]*( [A-Z][a-z]*)*)")
	match = pattern.match(s)
	if match:
	    yield [
	        match.start('x') + 1,
	        match.end('x') + 1,
	        match.start('y') + 1,
	        match.end('y') + 1,
	    ]

def ner(s):

    res = nlp.annotate(s, properties={
        'annotators': 'ner',
        'outputFormat': 'json'
    })  

    if not isinstance(res, dict):
        return

    for sen in res["sentences"]:
        begin = -1
        end = -1
        ner_prev = "O"
        for token in sen["tokens"]:
            ner_curr = str(token["ner"])
            if ner_curr == ner_prev:
                end = token["characterOffsetEnd"]
            else:
                if begin == -1 :
                    begin = token["characterOffsetBegin"]
                    end = token["characterOffsetEnd"]
                    ner_prev = ner_curr
                else:
                    yield [s, begin + 1, end + 1, ner_prev]
                    if ner_curr != "O":
                        begin = token["characterOffsetBegin"]
                        end = token["characterOffsetEnd"]
                        ner_prev = ner_curr
                    else:
                        begin = -1
                        end = -1
                        ner_prev = "O"
        if begin != -1:
            yield [s, begin + 1, end + 1, ner_prev]


if __name__ == "__main__":
    main()