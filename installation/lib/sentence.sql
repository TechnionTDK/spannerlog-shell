CREATE FUNCTION sentence (s text)
    RETURNS TABLE (sentence_index int, sentence_start int, sentence_end int)
AS $$
from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')
s = s.decode('utf-8','ignore').encode("utf-8")
res = nlp.annotate(s, properties={
    'annotators': 'ssplit',
    'outputFormat': 'json'
})  

if not isinstance(res, dict):
    return

for sen in res["sentences"]:
    yield [
        sen["index"],
        sen["tokens"][0]["characterOffsetBegin"] + 1,
        sen["tokens"][-1]["characterOffsetEnd"] + 1
    ]

$$ LANGUAGE plpythonu;
