CREATE FUNCTION sentence (s text)
    RETURNS TABLE (sentence_index int, sentence_start int, sentence_end int)
AS $$

from stanfordcorenlpspl import StanfordCoreNLP
import json

nlp = StanfordCoreNLP('http://localhost')
props={'annotators': 'ssplit'}
annotations = json.loads(nlp.annotate(s, properties=props))
for i, sen in enumerate(annotations["sentences"]):
	if sen["tokens"]:
		begin = sen["tokens"][0]["characterOffsetBegin"]
        end = sen["tokens"][-1]["characterOffsetEnd"]
    	yield [sen["index"], begin+1, end+1]

# from pycorenlp import StanfordCoreNLP
# nlp = StanfordCoreNLP('http://localhost:9000')
# res = nlp.annotate(s, properties={
#     'annotators': 'ssplit',
#     'outputFormat': 'json'
# })  

# if not isinstance(res, dict):
#     return

# for sen in res["sentences"]:
#     yield [
#         sen["index"],
#         sen["tokens"][0]["characterOffsetBegin"] + 1,
#         sen["tokens"][-1]["characterOffsetEnd"] + 1
#     ]

$$ LANGUAGE plpythonu;
