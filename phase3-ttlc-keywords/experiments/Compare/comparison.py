from os import listdir
from os.path import join
import sys
import HTMLParser
h=HTMLParser.HTMLParser()
predtag_dir = sys.argv[2]
acttag_dir = sys.argv[1]
txt=".txt"
tags = ".tags"
total_pred = 0
total_act =0
c1 = 0		# present in pred that are presnt in act 
for i in range(1,751):
	fname1 = join(acttag_dir,str(i)+tags)
	f1 = open(fname1,"r")
	r1 = f1.read()
	r1=h.unescape(r1)
	act_tag = [x[1:-1] for x in r1.split(',')]
	act_tag[len(act_tag)-1]= act_tag[len(act_tag)-1][:-1]
	total_act = total_act + len(act_tag)
	fname2 = join(predtag_dir,str(i)+txt)
	f2 = open(fname2,"r")
	r2= f2.readlines()
	pred_tag=[]
	for line in r2:
		pred_tag.append(line[:-2])
	total_pred = total_pred + len(pred_tag)
	for w in pred_tag:
		if w in act_tag:
			c1 = c1+1
print c1," ",total_pred," ",total_act		
print float(c1*1.0/total_pred)*100.0
print float(c1*1.0/total_act)*100.0	

