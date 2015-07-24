#!/usr/bn/env
#PYTHON CODE TO GENERATE STOPWORDS LIST AFTER EVALUATING RESULTS FROM THE RAKE ALGORITHM 
import nltk
from rake import RakeKeywordExtractor
import sys
from nltk.stem import WordNetLemmatizer
import re
import codecs
lemma_obj = WordNetLemmatizer()

def getAdjacencyFrequency(keywordList,content,words):
	adj_freq = {}
	prev_content = content
	tuple_list = tuple(x[0] for x in keywordList)
	pattern = re.compile('|'.join(tuple_list));
	content = pattern.sub(" 1 ",content)
	NUM = len(keywordList)
	for i in range(0,NUM):
			keywords = keywordList[i][0].split(' ')
			for word in keywords:
				adj_freq.setdefault(word,0)
				adj_freq[word] = adj_freq[word]+1
				
	words = nltk.word_tokenize(content)

	NUM = len(words)-1
	for i in range(1,NUM):
		if(words[i]!='1'):
			if(words[i-1]=='1' or  words[i+1]=='1'):
			 	adj_freq.setdefault(words[i],0)
			   	adj_freq[words[i]] = adj_freq[words[i]] +1
	return adj_freq		   
	

		
def getKeywordFrequency(keywordList):
	NUM = len(keywordList)
	keyword_freq={}
	for i in range(0,NUM):
		keywords = keywordList[i][0].split(' ')
		length = len(keywords)
		for word in keywords:
			keyword_freq.setdefault(word,0)
			keyword_freq[word] = keyword_freq[word] + 1
	return keyword_freq	

def completeRake(content):
	rakeObject  = RakeKeywordExtractor(set([]))
	keywordList = rakeObject.extract(content,True)
	words = nltk.word_tokenize(content)
	content_lemmatized = ""	
	words  = list(map(lambda x: lemma_obj.lemmatize(x),words))
	content_lemmatized = ' '.join(words)
	content = content_lemmatized
	freq = {}
	freq_dist  = nltk.FreqDist(words)
	keyword_freq=getKeywordFrequency(keywordList)
	adjacency_freq = getAdjacencyFrequency(keywordList,content,words)

	sortedFreqList = sorted(freq_dist.items(), key = lambda x: x[1],reverse=True)
	additional_stopwords=[]
	for key in sortedFreqList:
		keyword_freq.setdefault(key[0],0)
		adjacency_freq.setdefault(key[0],0)
		if(adjacency_freq[key[0]]>keyword_freq[key[0]]):
			additional_stopwords.append(key[0])
	additional_stopwords = set(additional_stopwords)
	newRakeObject = RakeKeywordExtractor(additional_stopwords)
	newKeywordList = newRakeObject.extract(content)
	for keywords in newKeywordList:
		print keywords

if __name__ == "__main__":
	#f = open(sys.argv[1],'r')
	f = codecs.open(sys.argv[1],'r',"iso8859-15")
	content = f.read()	
	content = content.encode('ascii','ignore')	
	content = re.sub(r"[1-9][0-9]*\.?[0-9]*",'',content)
