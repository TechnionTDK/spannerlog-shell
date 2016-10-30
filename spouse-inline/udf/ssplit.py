#!/usr/bin/env python

#. content          text
#. sentence_index   int
#. sentence_span    span 

from pycorenlp import StanfordCoreNLP

# nlp = StanfordCoreNLP('http://tdk2.cs.technion.ac.il:80')
nlp = StanfordCoreNLP('http://localhost:9000')

def ssplit(s):

    succ = False
    while succ == False:
        try:
            res = nlp.annotate(s, properties={
                'annotators': 'ssplit',
                'outputFormat': 'json'
            }) 
            succ = True 
        except:
            pass

    if res and isinstance(res, dict) and "sentences" in res:
        for sen in res["sentences"]:
            yield [
                s,
                sen["index"],
                sen["tokens"][0]["characterOffsetBegin"] + 1,
                sen["tokens"][-1]["characterOffsetEnd"] + 1
            ]
