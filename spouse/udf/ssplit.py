#!/usr/bin/env python

#. content          text
#. sentence_index   int
#. sentence_span    span 

import re

from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')

def ssplit(s):

    res = nlp.annotate(s, properties={
        'annotators': 'ssplit',
        'outputFormat': 'json'
    })  

    for sen in res["sentences"]:
        yield [
            s,
            sen["index"],
            sen["tokens"][0]["characterOffsetBegin"] + 1,
            sen["tokens"][-1]["characterOffsetEnd"] + 1
        ]
