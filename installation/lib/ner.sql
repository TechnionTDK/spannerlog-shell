CREATE FUNCTION ner (s text)
    RETURNS TABLE (entity_start int, entity_end int, category text)
AS $$
from stanfordcorenlpspl import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost')

entities = nlp.ner(s)

entity_start = -1
entity_end = -1
prev_category = "O"
for idx, (token, category, (m,n)) in enumerate(entities):
    if category == prev_category:
        entity_end = n
    else:
        if entity_start == -1 :
            entity_start = m
            entity_end = n
            prev_category = category
        else:
            yield [entity_start + 1, entity_end + 1, prev_category]
            if category != "O":
                entity_start = m
                entity_end = n
                prev_category = category
            else:
                entity_start = -1
                entity_end = -1
                ner_prev = "O"
if entity_start != -1:
    yield [entity_start + 1, entity_end + 1, prev_category]

$$ LANGUAGE plpythonu;

-- CREATE FUNCTION ner (s text)
--     RETURNS TABLE (entity_start int, entity_end int, category text)
-- AS $$
-- from pycorenlp import StanfordCoreNLP
-- nlp = StanfordCoreNLP('http://localhost:9000')
-- res = nlp.annotate(s, properties={
--     'annotators': 'ner',
--     'outputFormat': 'json'
-- })  

-- if not isinstance(res, dict):
--     return

-- for sen in res["sentences"]:
--     begin = -1
--     end = -1
--     ner_prev = "O"
--     for token in sen["tokens"]:
--         ner_curr = str(token["ner"])
--         if ner_curr == ner_prev:
--             end = token["characterOffsetEnd"]
--         else:
--             if begin == -1 :
--                 begin = token["characterOffsetBegin"]
--                 end = token["characterOffsetEnd"]
--                 ner_prev = ner_curr
--             else:
--                 yield [begin + 1, end + 1, ner_prev]
--                 if ner_curr != "O":
--                     begin = token["characterOffsetBegin"]
--                     end = token["characterOffsetEnd"]
--                     ner_prev = ner_curr
--                 else:
--                     begin = -1
--                     end = -1
--                     ner_prev = "O"
--     if begin != -1:
--         yield [begin + 1, end + 1, ner_prev]

-- $$ LANGUAGE plpythonu;
