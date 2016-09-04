#!/usr/bin/env python

#. context			text
#. sentence_index	int
#. sentence_text 	text 
#. tokens		 	text[] 
#. pos_tags		 	text[] 
#. ner_tags		 	text[] 


from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')

def nlp_markup(s):

	text = str(s.decode('ascii', 'ignore'))

	res = nlp.annotate(text, properties={
		'annotators': 'tokenize,ssplit,pos,ner',
		'outputFormat': 'json'
	})	

	for sen in res["sentences"]:
		yield [
			text,
			sen["index"], 
			str(''.join([token["originalText"]+token["after"] for token in sen["tokens"]])),
			[str(token["word"]) for token in sen["tokens"]],
			[str(token["pos"]) for token in sen["tokens"]],
			[str(token["ner"]) for token in sen["tokens"]],
		]
