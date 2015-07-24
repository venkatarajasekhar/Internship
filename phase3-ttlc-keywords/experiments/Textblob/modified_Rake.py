# this class is for ttlc queries 
# there is a question and question description 
#this is test 
# the first line contains question and all other following lines contain description of the question
# Adapted from: github.com/aneesha/RAKE/rake.py
from __future__ import division
from nltk.stem import WordNetLemmatizer
import operator
import nltk
import string
from stopwordList import getList

def isPunct(word):
  return len(word) == 1 and word in string.punctuation

def isNumeric(word):
  try:
    float(word) if '.' in word else int(word)
    return True
  except ValueError:
    return False

class RakeKeywordExtractor:

  def __init__(self):
	# self.stopwords = set(nltk.corpus.stopwords.words())
	self.stopwords  = getList()  
	self.top_fraction = 1.5 # consider top third candidate keywords by score

  def _generate_candidate_keywords(self, sentences):
    phrase_list = []
    lemma_obj = WordNetLemmatizer()	
    for sentence in sentences:
      words = map(lambda x: "|" if x in self.stopwords else x,
        nltk.word_tokenize(sentence.lower()))
      phrase = []
      for word in words:
        if word == "|" or isPunct(word):
          if len(phrase) > 0:
            phrase_list.append(phrase)
            phrase = []
        else:
          phrase.append(lemma_obj.lemmatize(word))
    return phrase_list

  def _calculate_word_scores(self, phrase_list):
    word_indi = []
    word_composite = []
    
    for phrase in phrase_list:
      degree = len(filter(lambda x: not isNumeric(x), phrase)) - 1
      for word in phrase:
        word_indi.append(word)
	if(degree>0):
		word_composite.append(word*degree)
    word_freq = nltk.FreqDist(word_indi) # with the indivudual word
    word_degree = nltk.FreqDist(word_composite)	#with the entire keyword composite 
    for word in word_freq.keys():
      word_degree[word] = word_degree[word] + word_freq[word] # itself
    # word score = deg(w) / freq(w)
    word_scores = {}
    for word in word_freq.keys():
      word_scores[word] = word_degree[word] / word_freq[word]
    return word_scores

  def _calculate_phrase_scores(self, phrase_list, word_scores):
    phrase_scores = {}
    for phrase in phrase_list:
      phrase_score = 0
      for word in phrase:
        phrase_score += word_scores[word]
      phrase_scores[" ".join(phrase)] = phrase_score
    return phrase_scores
    
  def extract(self, text,text2,incl_scores=False):	# text is answer, text2 is question
    sentences = nltk.sent_tokenize(text)
    sentences2 = nltk.sent_tokenize(text2)
    phrase_list = self._generate_candidate_keywords(sentences)
    phrase_list2 = self._generate_candidate_keywords(sentences2)
    phrase_list = phrase_list + 2*phrase_list2			# give 2 priority to keywords in the question 
    word_scores = self._calculate_word_scores(phrase_list)
    phrase_scores = self._calculate_phrase_scores(
      phrase_list, word_scores)
    sorted_phrase_scores = sorted(phrase_scores.iteritems(),
      key=operator.itemgetter(1), reverse=True)
    n_phrases = len(sorted_phrase_scores)
    if incl_scores:
      return sorted_phrase_scores[0:int(n_phrases/self.top_fraction)]
    else:
      return map(lambda x: x[0],
        sorted_phrase_scores[0:int(n_phrases/self.top_fraction)])

def test():
  	rake = RakeKeywordExtractor()
	folder="tt_queries/"
	for i in range(1,10):
		file_name = folder+str(i)+".txt"

		f = open(file_name,"r")
		question =f.readline() 			#assuming that the first line of the file contains question
		quesdes  = f.read()			# all other lines correspond to answers 
 		keywords = rake.extract(quesdes,question)
		print 5*"----",i,".txt",5*"----"
  		print keywords
  
if __name__ == "__main__":
  test()
