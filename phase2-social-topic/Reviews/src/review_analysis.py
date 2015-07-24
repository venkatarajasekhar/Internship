import nltk
import sys
import sys
from simnpchunk_rake import extractNP, extractKeywords
from nltk.collocations import *



qf = open(sys.argv[1])
df = open(sys.argv[2])
question = qf.read()
question= question.translate(None,"!()")
description = df.read()
description = description.translate(None,"!()")	
Q_NP = extractNP(question)
D_NP = extractNP(description)
F_NP = Q_NP + Q_NP + D_NP
keywords = extractKeywords(F_NP)

#obj = RakeKeywordExtractor()
#keywords = obj.extract(question,description,True)
wordlist = []
for key in keywords:
	temp = key[0].split(' ')
	for word in temp:
		wordlist.append(word)

print "TOP BIGRAMS"	
bigram_measures = nltk.collocations.BigramAssocMeasures()    
trigram_measures = nltk.collocations.TrigramAssocMeasures() 
bigram_finder = BigramCollocationFinder.from_words(wordlist);              #CREATE FINDER OBJECT 
scores = bigram_finder.score_ngrams( bigram_measures.raw_freq );        # WHAT MEASURE TO USE IS MENTIONED BY BIGRAM_MEASURE.RAW_FREQ
for i in range(0,50):
	print scores[i][0][0],scores[i][0][1]

print "\nTOP TRIGRAMS"

#FREQUENCY DISTRIBUTION OF TRIGRAM WORDS 
trigram_finder= TrigramCollocationFinder.from_words(wordlist);             #CREATE FINDER OBJECT
scores = trigram_finder.score_ngrams(trigram_measures.raw_freq);
for i in range(0,50):
	print scores[i][0][0],scores[i][0][1],scores[i][0][2]
