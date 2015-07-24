#### GRAMMER FROM SU NAM KIM AND MIN-YEN KAN ###########
########## USING RAKE TO SCORE THE KEYWRODS ###########

import nltk
import sys
import operator
from stopwordList import getList
from nltk.stem import WordNetLemmatizer
from rake import RakeKeywordExtractor
import codecs
import re
def extractNP(CONTENT):
	stopwords = getList()
	grammer = r"""
		NBAR:
			{<NN.*|JJ>*<NN.*>}  
		NP:
			{<NBAR>}
			{<NBAR><IN><NBAR>} 

		"""
	chunker = nltk.RegexpParser(grammer)	# create a chunker with the parser
#	sentences = nltk.sent_tokenize(CONTENT)
	lemmaobj = WordNetLemmatizer()
	words  = []
	paragraphs = [p for p in CONTENT.split('\n') if p]
	for para in paragraphs:
		sentences = [s for s in nltk.sent_tokenize(para) if s]
		for sentence in sentences:
			word = [w.lower() for w in nltk.word_tokenize(sentence)]
			taggedwords = nltk.pos_tag(word)
			tree = chunker.parse(taggedwords)
			temp = [] 
			for subtree in tree.subtrees():
				if subtree.label() == "NP":
					for leaves in subtree.leaves():
						w = leaves[0].lower()
						if w not in stopwords:
							w = lemmaobj.lemmatize(w)
							temp.append(w)
					if temp!=[]:
						words.append(temp)
						temp = []
	return words 			

def extractKeywords(phrase_list):
	RAKE_OBJ = RakeKeywordExtractor(set([]))
	word_scores = RAKE_OBJ._calculate_word_scores(phrase_list)
	phrase_scores = RAKE_OBJ._calculate_phrase_scores(phrase_list, word_scores)
	sorted_phrase_scores = sorted(phrase_scores.iteritems(),key=operator.itemgetter(1), reverse=True)
	n_phrases = len(sorted_phrase_scores)
	return [x[0] for x in sorted_phrase_scores[0:int(n_phrases)]]

if __name__=="__main__":
	#f = open(sys.argv[1],"r")
	f = codecs.open(sys.argv[1],"r","iso8859-15")
	CONTENT = f.read()
	CONTENT = CONTENT.encode('ascii','ignore')
	CONTENT = re.sub(r"[1-9][0-9]*\.?[0-9]*",'',CONTENT)
	words = extractNP(CONTENT)
	keywords = extractKeywords(words)
	print keywords
