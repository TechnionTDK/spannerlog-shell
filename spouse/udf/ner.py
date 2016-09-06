#!/usr/bin/env python

#. content          text
#. span             span 
#. ner_tag          text 


from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')

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
        ner_tag = "O"
        for token in sen["tokens"]:
            ner_tag_inner = str(token["ner"])
            if ner_tag_inner == ner_tag:
                end = token["characterOffsetEnd"] + 1
            else:
                if begin == -1 :
                    begin = token["characterOffsetBegin"] + 1
                    end = token["characterOffsetEnd"] + 1
                    ner_tag = ner_tag_inner
                else:
                    yield [s, begin, end, ner_tag]
                    if ner_tag_inner != "O":
                        begin = token["characterOffsetBegin"] + 1
                        end = token["characterOffsetEnd"] + 1
                        ner_tag = ner_tag_inner
                    else:
                        begin = -1
                        end = -1
                        ner_tag = "O"
        if begin != -1:
            yield [s, begin, end, ner_tag]

            # yield [
            #   s,
            #   token["characterOffsetBegin"], 
            #   token["characterOffsetEnd"], 
            #   str(token["ner"]),
            # ]
