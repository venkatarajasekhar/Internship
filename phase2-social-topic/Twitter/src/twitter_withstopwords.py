# PYTHON CODE FOR READING SET OF TWEETS FROM A CSV FILE AND THE THIRD COLUM SHOULD BE THE TWEETS 
# REFER TO THE VODAFONEIN.CSV FOR FURTHER INFORMATION ABOUT THE FORMAT 
# TOKENIZE -> REMOVE STOP WORDS -> STEMMING -> USING FREQUENCY DISTRUBUTION -> PICK THE TOP WORDS

# AUTHOR : SRIHARSHA V
# PURPOSE: FOR IDENTIFYING IMPORTANT WORDS IN A SET OF TWEETS





# IMPORTING REQUIRED MODULES
import nltk as nltk					# MAIN NLTK PACKAGE
import codecs						# FOR READING THE FILE IN UTF-8 FORMAT	
import HTMLParser 					# FOR REPLACING THE HTML FORMATS
import sys						# FOR THE COMMAND LINE INPUTS
import re 						# FOR PATTERN MATCHING
from stopwords import completeRake


if(len(sys.argv)!=2):
	print "Input CSV file not give"
	exit()
f=codecs.open(sys.argv[1],encoding='utf-8');				# FILE CONTAINING TWEETS
r = f.readlines();				# READLINES FROM THE FILE 
NUM_TWEETS = len(r);				#NUMBER OF TWEEETS IN THE INPUT 

h = HTMLParser.HTMLParser(); 

p1 = re.compile(r"\bw+hen+\b|\bw+here+\b|\bh+ow+\b|^do\b|^can\b|\bw+hat+\b|\bw+ho+\b|\bw+hy+\b|\?+|\bneed\b|\bneeded\b|help|want|wanted|look+|^is|^are|^does");



content = ""							#ARRAY FOR TWEETS 
words = [] 							# ARRAY AFTER TOKENIZATION AND STOP WORD REMOVAL
count = 0
all_tweets=""
for i in range(0,NUM_TWEETS):
	r[i] = h.unescape(r[i]);				# REMOVE HTML OBJECTS USING HTMLPARSER OBJECTS
	r[i] = r[i].encode('ascii','ignore');			# CONVERT FROM UNICODE TO STRING
	temp = r[i].lower()
	all_tweets = all_tweets + "\n" + temp
	m1=p1.search(temp)
	if m1!=None:
		x=((r[i].split(','))[3:])# STORE ALL TWEETS IN LOWER CASE. REMOVE USERNAME.
		temp=""
		for state in x:
			temp = temp +" "+state
#print temp
		content=content + "\n" + temp.lower()			# STORE ALL TWEETS IN LOWER CASE. REMOVE USERNAME.
		
completeRake(content)      				
















