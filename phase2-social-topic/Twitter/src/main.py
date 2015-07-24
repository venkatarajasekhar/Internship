# PYTHON CODE FOR READING SET OF TWEETS FROM A CSV FILE AND THE THIRD COLUM SHOULD BE THE TWEETS 
# REFER TO THE VODAFONEIN.CSV FOR FURTHER INFORMATION ABOUT THE FORMAT 
# TOKENIZE -> REMOVE STOP WORDS -> STEMMING -> USING FREQUENCY DISTRUBUTION -> PICK THE TOP WORDS

# AUTHOR : SRIHARSHA V
# PURPOSE: FOR IDENTIFYING IMPORTANT WORDS IN A SET OF TWEETS





# IMPORTING REQUIRED MODULES
import nltk as nltk					# MAIN NLTK PACKAGE
from nltk.corpus import stopwords			# PACKAGE FOR STOPWORDS
from nltk.stem.lancaster import LancasterStemmer	# FOR STEMMING
from nltk.collocations import *				# FOR COLLOCATION STATISTICS
import codecs						# FOR READING THE FILE IN UTF-8 FORMAT	
import HTMLParser 					# FOR REPLACING THE HTML FORMATS
import sys						# FOR THE COMMAND LINE INPUTS
import re 						# FOR PATTERN MATCHING
from nltk.stem import WordNetLemmatizer			# FOR LEMMETIZATION



if(len(sys.argv)!=2):
	print "Input CSV file not give"
	exit()
f=codecs.open(sys.argv[1],encoding='utf-8');				# FILE CONTAINING TWEETS
r = f.readlines();				# READLINES FROM THE FILE 
NUM_TWEETS = len(r);				#NUMBER OF TWEEETS IN THE INPUT 

bigram_measures = nltk.collocations.BigramAssocMeasures()	#BIGRAM OBJECT
trigram_measures = nltk.collocations.TrigramAssocMeasures()	#TRIGRAM OBJECT 	
wordnet_lemmatizer = WordNetLemmatizer()			# LEMMETIZATION OBJECT 
h = HTMLParser.HTMLParser();					# HTML PARSER OBJECT

p1 = re.compile(r"\bw+hen+\b|\bw+here+\b|\bh+ow+\b|^do\b|^can\b|\bw+hat+\b|\bw+ho+\b|\bw+hy+\b|\?+|\bneed\b|\bneeded\b|help|want|wanted|look+|^is|^are|^does");


# TOKENIZATION AND ADDING TO THE DICTIONARY
# ENTRY FOR A WORD ONLY ONCE PER TWEET 

# LIST OF STOP WORDS
extra_stopwords = set(('we','us','please','-','.','','u','don\'t'));		# EXTRA STOP WORDS TO BE REMOVED
stop = set(stopwords.words('english'));
stop=stop.union(extra_stopwords);				# ADDING EXTRA STOP WORDS 
st = LancasterStemmer();					#STEMMER OBJECTS
tweets = []							#ARRAY FOR TWEETS 
words = [] 							# ARRAY AFTER TOKENIZATION AND STOP WORD REMOVAL
count = 0
file_write = open('query','w+');
all_tweets=""
for i in range(0,NUM_TWEETS):
	r[i] = h.unescape(r[i]);				# REMOVE HTML OBJECTS USING HTMLPARSER OBJECTS
	r[i] = r[i].encode('ascii','ignore');			# CONVERT FROM UNICODE TO STRING
	temp = r[i].lower()
	all_tweets = all_tweets + "\n" + temp
	m1=p1.search(temp)
	if m1!=None:
		
		r[i] = r[i].translate(None,"?.!\r\n-:&)(");			# REPLACE CERTAIN CHARACTERS WITH NONE
		tweets.append(((r[i].split(','))[3]).lower())			# STORE ALL TWEETS IN LOWER CASE. REMOVE USERNAME.
		s=[wordnet_lemmatizer.lemmatize(z) for z in (tweets[count].split(' '))[1:] if z not in stop]	# REMOVING STOP WORDS 
		words = words + s;
		count = count + 1
      				
print count 
#file_write.write(all_tweets)

# FREQUENCY DISTRIBUTION OF SINGLE WORDS
freq_words = nltk.FreqDist(words);
for i in freq_words.most_common(50):
	print i[0],":",i[1]

print "\n \n Most Frequent Bigrams"
#FREQUENCY DISTRIBUTION OF BIGRAM WORDS 	
bigram_finder = BigramCollocationFinder.from_words(words);		#CREATE FINDER OBJECT 
scores = bigram_finder.score_ngrams( bigram_measures.raw_freq );	# WHAT MEASURE TO USE IS MENTIONED BY BIGRAM_MEASURE.RAW_FREQ
for i in range(0,50):
	print scores[i][0][0],"",scores[i][0][1]

#FREQUENCY DISTRIBUTION OF TRIGRAM WORDS 
trigram_finder= TrigramCollocationFinder.from_words(words);		#CREATE FINDER OBJECT
scores = trigram_finder.score_ngrams(trigram_measures.raw_freq);	# USE FREQUENCY AS A MEASURE 
print "\n \n Most Frequent Trigrams"
for i in range(0,50):
	print scores[i][0][0],scores[i][0][1],scores[i][0][2]















