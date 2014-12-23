from MyMaxEnt import *
#from random import randint

#sentances = # list [ [history1,2,3],[hisofsent2-1,2,3] ]
#tag_list = []

piD={}
bpD={}



def pi(index,prevtag,tag):
	global piD
	print piD
	#raw_input()
	if(str(index)+"-"+str(prevtag)+"-"+str(tag) in piD.keys()):
		return piD[str(index)+"-"+str(prevtag)+"-"+str(tag)]
	else :
		return 0

def setPi(index,prevtag,tag,value):
	global piD
	piD[str(index)+"-"+str(prevtag)+"-"+str(tag)] = value;



def bp(index,prevtag,tag):
	global bpD
	return bpD[str(index)+"-"+str(prevtag)+"-"+str(tag)]

def setBp(index,prevtag,tag,value):
	global bpD
	bpD[str(index)+"-"+str(prevtag)+"-"+str(tag)] = value;




setPi(-1,"*","*",1)
storeTag = 0
storePrevTag = 0
vi_tag_list = ["*","Org","Phone","Feature","Family","Other","OS","Version","Price"]	


def vitterbi(sentance):
	global storeTag
	global sents
	global storePrevTag
	global vi_tag_list
	for i in range(len(sents[sentance])) :
		for tag in vi_tag_list:					
			for prevTag in vi_tag_list:
				maximum = -3200;
				back = ""
				for prevprevTag	in vi_tag_list:			
					h = (prevprevTag,prevTag,sentance,i)
					#print h			
					q = maxent.p_y_given_x(h,tag)
					l = pi(i-1,prevTag,tag)
					#print q,l					
					#if(not l): continue
					#raw_input()				
					answer = q * pi(i-1,prevTag,tag)
					if(maximum < answer):
										
						maximum = answer
						back	= str(prevprevTag[:])
						print back, maximum						
						#raw_input()					
						storePrevTag = prevTag
						storeTag = tag
				#print i,prevTag,tag,maximum,back				
				setPi(i-1,prevTag,tag,maximum)
				setBp(i-1,prevTag,tag,back)

	finalTag = {}
	
	finalTag[len(sents[sentance])-1] = storeTag
	finalTag[len(sents[sentance])-2] = storePrevTag

	for i in range(len(sents[sentance])-3,-1,-1):
		finaltag[i] = bp(i+2,finalTag[i+1],finalTag[i+2])

	print sentance
	print finalTag			 			
				#q * vetterbi()
			
		#	l = vitterbi(prev)

#sen = "Do you have an android phone costing lesser than Rs 1000 ?"
#sen = sen.split(" ");
senNo = randint(0,len(sents)-1)
print sents[senNo]
vitterbi(senNo)


