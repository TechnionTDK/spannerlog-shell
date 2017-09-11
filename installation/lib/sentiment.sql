CREATE FUNCTION sentiment (s text)
    RETURNS TABLE (sentence_start int, sentence_end int, label text, value int)
AS $$

from stanfordcorenlpspl import StanfordCoreNLP
import json

nlp = StanfordCoreNLP('http://localhost')
props={'annotators': 'sentiment'}
annotations = json.loads(nlp.annotate(s, properties=props))
for i, sen in enumerate(annotations["sentences"]):
    if sen["tokens"]:
        begin = sen["tokens"][0]["characterOffsetBegin"]
        end = sen["tokens"][-1]["characterOffsetEnd"]
        yield [begin, end, sen["sentiment"], sen["sentimentValue"]]

$$ LANGUAGE plpythonu;
