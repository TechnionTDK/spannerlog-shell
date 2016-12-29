CREATE FUNCTION ner (s text)
    RETURNS TABLE (entity_start int, entity_end int, category text)
AS $$
from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')
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
                yield [begin + 1, end + 1, ner_prev]
                if ner_curr != "O":
                    begin = token["characterOffsetBegin"]
                    end = token["characterOffsetEnd"]
                    ner_prev = ner_curr
                else:
                    begin = -1
                    end = -1
                    ner_prev = "O"
    if begin != -1:
        yield [begin + 1, end + 1, ner_prev]

$$ LANGUAGE plpythonu;
