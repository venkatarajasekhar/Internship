#AUTOMATIC TAGGER REQUEIRES MAPS A TTLC QUERY TO ONE OR MANY GIVEN 
# Author : Sriharsha
"""
TAKES TWO COMMAND LINE ARGUMENTS 
THE FIRST COMMAND LINE ARGUMENT IS THE TAG LIST AND THE SECOND IS A FILE CONTANING SINGLE TTLC POST
IT IS ASSUMED THE FILE CONTANING TTLC POST HAS QUESTION IN THE FIRST LINE FOLLOWED BY THE DESCRIPTION OF THE QUESTION
CALLS THE CLASS IN MODIFIED_RAKE.PY FILE
THE OUTPUT WOULD BE SET OF TAGS FOR THAT POST 
"""
from modified_Rake import RakeKeywordExtractor
import nltk
import distance
from nltk.stem import WordNetLemmatizer
import sys
import time
import itertools
import Levenshtein
from simnpchunk_rake import extractNP, extractKeywords 
import HTMLParser
from os import listdir
from os.path import isfile, join
import codecs
class AssignTags:
	def __init__(self,tags):
		self.tags = tags
		self.lemobj = WordNetLemmatizer()
		self.worddict = {}
		self.taglist = []
		self.taglem = []
		i=0
		for tag in tags:
			words = tag.split(' ')
			words = words[:-1]
			wordlist=[self.lemobj.lemmatize(word) for word in words]
			array = []
			array.append(wordlist)
			array.append(i)
			self.taglist.append(array)
			tempstr=""
			for word in wordlist:
				tempstr=tempstr+word+" "
			array=[]
			array.append(tempstr[:-1])
			array.append(i)
			self.taglem.append(array)	
			i=i+1	
	def getKeywordList(self,question,description):
		RAKEOBJ = RakeKeywordExtractor()
		return_list = RAKEOBJ.extract(description,question,False)
		keywords = [r for r in return_list]
		return keywords

	def getTags(self,keywords):
		predtags=set([])
		keywordlist = []
#		for keyword in keywords:
#			keywordlist.append(keyword.split(' '))
		keywordlist = [set(keyword.split(' ')) for keyword in keywords]
		taglist_set = [(set(wordlist[0]),wordlist[1]) for wordlist in self.taglist]
#	print taglist_set 
################### check if a tag is completely in a keyword#################################
		
		start_time = time.time()
		for wordlist in taglist_set:
			flag=0
			for keyword in keywordlist:
				if((wordlist[0])<=(keyword)):
					flag=1
					break
			if(flag==1):
				predtags.add(self.tags[wordlist[1]])
############################################## step completed###############################		
		
#	r = [tag[1] for tag,keyword in itertools.product(self.taglem,keywords) if((1-Levenshtein.ratio(tag[0],keyword))<0.2)]
		for keyword in keywords:
			for tag in self.taglem:
				score = Levenshtein.ratio(unicode(tag[0]),unicode(keyword))
				if(score>0.8):
			  		predtags.add(self.tags[tag[1]])
		return set(predtags)
				
		# for each keyword see the tag with minimum value, 
					

if __name__=="__main__":
	"""
	h = HTMLParser.HTMLParser()
#	start_time = time.time()
	f1 = open(sys.argv[1],"r")
	f2 = open(sys.argv[2],"r")
	l1 = f1.readlines()
	question = f2.readline()
	description = f2.read()
	description=description.translate(None,"`\'\"-")
	CONTENT  = question + "\n" + question+ "\n" + description
	tags=[]
	for line in l1:
		tags.append(line[:-1])
	obj = AssignTags(tags)
	np = extractNP(CONTENT)
	keywords = extractKeywords(np)
#	keywords=obj.getKeywordList(question,description)
	tags=obj.getTags(keywords)
#	print time.time()-start_time
	for tag in tags:
		print tag
	"""	
	h=HTMLParser.HTMLParser()
#	start_time = time.time()
	f1 = open(sys.argv[1],"r")
	l1 = f1.readlines()
	tags=[]
	for line in l1:
		tags.append(line[:-1])
	obj = AssignTags(tags)
	input_dir = sys.argv[2]	# input directory
	output_dir= sys.argv[3]	# output directory
	for f in listdir(input_dir):
		fname = join(input_dir,f)
		f2 = codecs.open(fname,"r",encoding="utf-8")
		question = f2.readline()
		question = question.encode('ascii','ignore')
		question = h.unescape(question)
		description = f2.read()
		description = description.encode('ascii','ignore')
		description = h.unescape(description)
		CONTENT  = question + "\n" + question+ "\n" + description
		np1 = extractNP(CONTENT)
		keywords = extractKeywords(np1)
		tags=obj.getTags(keywords)
		fname = join(output_dir,f)
		f3 = open(fname,"w")
		for tag in tags:
			f3.write(tag+"\n")
		f2.close()
		f3.close() 

		
